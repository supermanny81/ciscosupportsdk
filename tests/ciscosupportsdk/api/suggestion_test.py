import pytest

from ciscosupportsdk.api.softwaresuggestion import _compatible_params
from fixtures import *  # noqa


class TestCompatibleParams:
    def test_multi_value_inputs_are_comma_joined(self):
        # The service expects a single comma separated value; passing a list
        # straight to requests encodes it as repeated query parameters.
        params = _compatible_params(
            None, None, ["ipsec", "ssl"], ["WS-C3560", "WS-C3750"]
        )

        assert params["supportedFeatures"] == "ipsec,ssl"
        assert params["supportedHardware"] == "WS-C3560,WS-C3750"

    def test_omitted_inputs_stay_none(self):
        params = _compatible_params("img.bin", "15.0(2)", None, None)

        assert params == {
            "currentImage": "img.bin",
            "currentRelease": "15.0(2)",
            "supportedFeatures": None,
            "supportedHardware": None,
        }

    def test_too_many_features_is_rejected(self):
        with pytest.raises(ValueError, match="Too many supported_features"):
            _compatible_params(None, None, [f"f{i}" for i in range(11)], None)

    def test_over_long_feature_list_is_rejected(self):
        with pytest.raises(ValueError, match="maximum length"):
            _compatible_params(None, None, ["x" * 100] * 10, None)


SUGGESTIONS = {
    "status": "Success",
    "paginationResponseRecord": {
        "pageIndex": 1,
        "lastIndex": 1,
        "totalRecords": 1,
        "pageRecords": 1,
    },
    "productList": [
        {
            "id": "1",
            "product": {
                "basePID": "WS-C3560-48PS-S",
                "mdfId": "283612677",
                "productName": "Catalyst 3560 48 10/100 PoE + 4 SFP",
                "softwareType": "IOS Software",
            },
            "suggestions": [
                {
                    "id": "1",
                    "isSuggested": "Y",
                    "releaseFormat1": "15.0(2)SE11",
                    "releaseFormat2": "15.0.2SE11",
                    "releaseDate": "2017-05-19",
                    "majorRelease": "15.0",
                    "releaseTrain": "SE",
                    "releaseLifeCycle": "GD",
                    "relDispName": "15.0(2)SE11",
                    "trainDispName": "15.0SE",
                    "images": [
                        {
                            "imageName": "c3560-ipbasek9-mz.150-2.SE11.bin",
                            "imageSize": "16000000",
                            "requiredDRAM": "128 MB",
                            "requiredFlash": "32 MB",
                        }
                    ],
                }
            ],
        }
    ],
}

COMPATIBLE = {
    "status": "Success",
    "paginationResponseRecord": {"pageIndex": 1, "lastIndex": 1},
    "suggestions": [{"id": "1", "releaseFormat1": "15.0(2)SE11"}],
}


class TestSoftwareSuggestionApi:
    def test_suggestions_and_image_by_product_ids(self, api_factory):
        api, client = api_factory(SUGGESTIONS)

        result = next(
            api.suggestion.get_suggestions_and_image_by_product_ids(
                ["WS-C3560-48PS-S"]
            )
        )

        assert result.product.base_pid == "WS-C3560-48PS-S"
        assert result.suggestions[0].images[0].name.endswith(".bin")
        # Suggestion is a camelCase API and must be paged with pageIndex.
        assert client.params() == {"pageIndex": 1}
        assert "/suggestions/software/productIds/" in client.urls[0]

    def test_suggestions_by_product_ids(self, api_factory):
        api, client = api_factory(SUGGESTIONS)

        next(
            api.suggestion.get_suggestions_by_product_ids(["WS-C3560-48PS-S"])
        )

        assert "/suggestions/releases/productIds/" in client.urls[0]

    def test_suggestions_and_image_by_mdf_ids(self, api_factory):
        api, client = api_factory(SUGGESTIONS)

        next(
            api.suggestion.get_suggestions_and_image_by_mdf_ids(["283612677"])
        )

        assert "/suggestions/software/mdfIds/283612677" in client.urls[0]

    def test_suggestions_by_mdf_ids(self, api_factory):
        api, client = api_factory(SUGGESTIONS)

        next(api.suggestion.get_suggestions_by_mdf_ids(["283612677"]))

        assert "/suggestions/releases/mdfIds/283612677" in client.urls[0]

    def test_compatible_by_product_id(self, api_factory):
        api, client = api_factory(COMPATIBLE)

        result = next(
            api.suggestion.get_compatible_by_product_id(
                "WS-C3560-48PS-S",
                supported_features=["ipsec", "ssl"],
                supported_hardware=["WS-C3560"],
            )
        )

        assert result.release_format1 == "15.0(2)SE11"
        assert client.params()["supportedFeatures"] == "ipsec,ssl"
        assert client.params()["supportedHardware"] == "WS-C3560"

    def test_compatible_by_mdf_id(self, api_factory):
        api, client = api_factory(COMPATIBLE)

        next(api.suggestion.get_compatible_by_mdf_id("283612677"))

        assert "/suggestions/compatible/mdfId/283612677" in client.urls[0]

    def test_success_response_needs_no_error_block(self, api_factory):
        # errorDetailsResponse used to be a required field, which rejected
        # every successful response the service returned.
        api, _ = api_factory(SUGGESTIONS)

        result = next(
            api.suggestion.get_suggestions_by_product_ids(["WS-C3560-48PS-S"])
        )

        assert result.suggestions[0].error_details_response is None

    def test_too_many_product_ids_is_rejected(self, api):
        with pytest.raises(ValueError, match="product_ids"):
            next(api.suggestion.get_suggestions_by_product_ids(["PID"] * 11))
