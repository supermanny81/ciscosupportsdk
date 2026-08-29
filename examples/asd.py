import os

from ciscosupportsdk.api import CiscoSupportAPI

CS_API_KEY = os.getenv("CS_API_KEY")
CS_API_SECRET = os.getenv("CS_API_SECRET")

cs = CiscoSupportAPI(CS_API_KEY, CS_API_SECRET)

PID = "ASR10012XOC3POS-RF"

# Look up the software metadata for a product and the release it is running.
# ASD nests its results product -> software type -> OS -> release -> image.
for record in cs.asd.get_software_by_pid_and_release(PID, "5.4.3"):
    for product in record.products:
        for software_type in product.software_types:
            for os_entry in software_type.operating_systems:
                for release in os_entry.releases:
                    for image in release.images:
                        print(
                            f"{release.version}: {image.name} "
                            f"({image.size}) {image.image_guid}"
                        )

# Check the current status of images you already have on hand. Names the
# service does not recognise come back in `invalid_images` rather than as an
# error.
status = cs.asd.get_software_status_by_image(
    ["c1700-y-mz.124-13a.bin", "not-a-real-image.bin"]
)
print(f"unrecognised images: {status.invalid_images}")

# Downloading is a two step flow: the metadata call above yields the image
# GUIDs and the transaction id that the download call needs.
downloads = cs.asd.get_download_urls(
    pid=PID,
    mdf_id="286305578",
    metadata_trans_id="617462102359722937",
    image_guids=["25856C5890AE73F8EDBEEDA441EC901F8FC8362E"],
)

# When an agreement has not been accepted yet, the URLs are withheld and an
# acceptance form comes back instead. Accept it, then ask again.
if downloads.acceptance_form is not None:
    print("K9/EULA acceptance required")
    print(cs.asd.get_k9_agreement().status_message)
    cs.asd.accept_k9_agreement(file_names=["asr1000.bin"])
    cs.asd.accept_eula_agreement(file_names=["asr1000.bin"])
    downloads = cs.asd.get_download_urls(
        pid=PID,
        mdf_id="286305578",
        metadata_trans_id="617462102359722937",
        image_guids=["25856C5890AE73F8EDBEEDA441EC901F8FC8362E"],
    )

for download in downloads.items:
    print(f"{download.image_name}: {download.url}")
