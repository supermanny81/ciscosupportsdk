import pytest

from ciscosupportsdk.api.asd import AutomatedSoftwareDistributionApi
from ciscosupportsdk.models.asd import ComplianceStatus
from fixtures import *  # noqa

METADATA_PAGE = {
    "pagination": {
        "pageIndex": 1,
        "lastIndex": 1,
        "totalRecords": 1,
        "pageRecords": 1,
    },
    "metadataTransId": "617462102359722937",
    "metadata": [
        {
            "pid": "ASR10012XOC3POS-RF",
            "products": [
                {
                    "mdfId": "286305578",
                    "softwareTypes": [
                        {
                            "softwareTypeName": "IOS XE Software",
                            "operatingSystems": [
                                {
                                    "releases": [
                                        {
                                            "version": "5.4.3",
                                            "images": [
                                                {
                                                    "imageGuid": "25856C58",
                                                    "name": "asr1000.bin",
                                                    "md5": "abc123",
                                                }
                                            ],
                                        }
                                    ]
                                }
                            ],
                        }
                    ],
                }
            ],
        }
    ],
}


class FakeSession:
    """Records what the API layer sends without touching the network."""

    def __init__(self, responses):
        self._responses = list(responses)
        self.posts = []
        self.gets = []

    def _post(self, path, json=None, params=None):
        self.posts.append((path, json))
        return self._responses.pop(0)

    def _get(self, path, params):
        self.gets.append((path, params))
        return self._responses.pop(0)


@pytest.fixture
def asd_factory():
    def _make(responses):
        session = FakeSession(responses)
        return AutomatedSoftwareDistributionApi(session), session

    return _make


class TestAsdApi:
    def test_metadata_by_pid_and_release(self, asd_factory):
        asd, session = asd_factory([METADATA_PAGE])

        records = list(
            asd.get_software_by_pid_and_release(
                "ASR10012XOC3POS-RF", "5.4.3", per_page=1
            )
        )

        path, body = session.posts[0]
        assert path == "/software/v4.0/metadata/pidrelease"
        assert body == {
            "pid": "ASR10012XOC3POS-RF",
            "currentReleaseVersion": "5.4.3",
            "outputReleaseVersion": "latest",
            "pageIndex": 1,
            "perPage": 1,
        }

        image = (
            records[0]
            .products[0]
            .software_types[0]
            .operating_systems[0]
            .releases[0]
            .images[0]
        )
        assert image.name == "asr1000.bin"
        assert image.md5 == "abc123"

    def test_metadata_pagination(self, asd_factory):
        first = dict(METADATA_PAGE)
        first["pagination"] = {"pageIndex": 1, "lastIndex": 2}
        second = dict(METADATA_PAGE)
        second["pagination"] = {"pageIndex": 2, "lastIndex": 2}

        asd, session = asd_factory([first, second])

        records = list(
            asd.get_software_by_pid_and_image("ASR1000", ["asr1000.bin"])
        )

        assert len(records) == 2
        assert [body["pageIndex"] for _, body in session.posts] == [1, 2]
        # perPage is left out when the caller does not ask for it
        assert "perPage" not in session.posts[0][1]

    def test_software_status_surfaces_invalid_images(self, asd_factory):
        asd, session = asd_factory(
            [{"invalidImages": ["nope.bin"], "metadata": []}]
        )

        response = asd.get_software_status_by_image(
            ["c1700-y-mz.124-13a.bin", "nope.bin"]
        )

        assert session.posts[0][0] == "/software/v4.0/metadata/images"
        assert response.invalid_images == ["nope.bin"]

    def test_download_reports_pending_acceptance_form(self, asd_factory):
        asd, session = asd_factory(
            [
                {
                    "sessionId": "abc",
                    "acceptanceForm": {"k9Content": "..."},
                    "downloads": [],
                }
            ]
        )

        response = asd.get_download_urls(
            "ACS-1800-RM-19=", "286305578", "617462102359722937", ["25856C58"]
        )

        path, body = session.posts[0]
        assert path == "/software/v4.0/download/pidimage"
        assert body["metadataTransId"] == "617462102359722937"
        assert body["imageGuids"] == ["25856C58"]
        # The caller has to be able to see that an agreement is outstanding.
        assert response.acceptance_form is not None
        assert response.items == []

    def test_downloads_yields_urls(self, asd_factory):
        asd, _ = asd_factory(
            [{"downloads": [{"url": "https://dl.cisco.com/x", "token": "t"}]}]
        )

        downloads = list(asd.get_downloads("PID", "MDF", "TRANS", ["GUID"]))

        assert downloads[0].url == "https://dl.cisco.com/x"

    def test_get_k9_agreement(self, asd_factory):
        asd, session = asd_factory(
            [
                {
                    "statusCode": "0",
                    "k9Content": "...",
                    "userDetails": {"userId": "testuser"},
                }
            ]
        )

        agreement = asd.get_k9_agreement()

        assert session.gets[0][0] == "/software/v4.0/compliance/k9"
        assert agreement.user_details.user_id == "testuser"

    def test_accept_k9_agreement(self, asd_factory):
        asd, session = asd_factory([{"statusCode": "0"}])

        asd.accept_k9_agreement(file_names=["a.tar.gz", "b.tar.gz"])

        _, body = session.posts[0]
        assert body["status"] == "Accepted"
        assert body["busFunction"] == "COMM_OR_CIVIL"
        # Multi-value inputs go over as a single comma separated value.
        assert body["fileNames"] == "a.tar.gz,b.tar.gz"
        assert "declineComments" not in body

    def test_accept_eula_agreement(self, asd_factory):
        asd, session = asd_factory([{"statusCode": "0"}])

        ack = asd.accept_eula_agreement(file_names=["anyconnect.tar.gz"])

        path, body = session.posts[0]
        assert path == "/software/v4.0/compliance/eula"
        assert body == {
            "status": "Accepted",
            "fileNames": "anyconnect.tar.gz",
        }
        assert ack.status_code == "0"

    @pytest.mark.parametrize(
        "method", ["accept_k9_agreement", "accept_eula_agreement"]
    )
    def test_declining_requires_comments(self, asd_factory, method):
        asd, _ = asd_factory([{"statusCode": "0"}])

        with pytest.raises(ValueError):
            getattr(asd, method)(status=ComplianceStatus.DECLINED)

    def test_declining_with_comments_is_sent(self, asd_factory):
        asd, session = asd_factory([{"statusCode": "0"}])

        asd.accept_eula_agreement(
            status=ComplianceStatus.DECLINED, decline_comments="no thanks"
        )

        _, body = session.posts[0]
        assert body["status"] == "Declined"
        assert body["declineComments"] == "no thanks"

    def test_get_eula_agreement(self, asd_factory):
        asd, session = asd_factory(
            [{"statusCode": "0", "eulaContent": "...", "subAppVersion": "4.0"}]
        )

        agreement = asd.get_eula_agreement()

        assert session.gets[0][0] == "/software/v4.0/compliance/eula"
        assert agreement.eula_content == "..."

    def test_declining_k9_sends_comments_and_files(self, asd_factory):
        asd, session = asd_factory([{"statusCode": "0"}])

        asd.accept_k9_agreement(
            file_names=["anyconnect-k9.tar.gz"],
            status=ComplianceStatus.DECLINED,
            decline_comments="not permitted in this region",
        )

        _, body = session.posts[0]
        assert body["status"] == "Declined"
        assert body["declineComments"] == "not permitted in this region"
        assert body["fileNames"] == "anyconnect-k9.tar.gz"
