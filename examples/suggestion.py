import os

from ciscosupportsdk.api import CiscoSupportAPI

CS_API_KEY = os.getenv("CS_API_KEY")
CS_API_SECRET = os.getenv("CS_API_SECRET")

cs = CiscoSupportAPI(CS_API_KEY, CS_API_SECRET)

# get the suggested realease and image
for item in cs.suggestion.get_suggestions_and_image_by_product_ids(
    ["ASR-903", "CISCO2811", "N7K-C7018"]
):
    print(
        f"Suggestion for {item.product.product_name} "
        f"({item.product.base_pid})..."
    )
    for suggestion in item.suggestions:
        for image in suggestion.images:
            print(
                f"- {suggestion.rel_display_name}: {image.name} "
                f"{image.size}bytes\n"
                f"  - {image.feature_set}"
            )
    print("\n")


# get the suggested realease and image
for item in cs.suggestion.get_suggestions_by_product_ids(
    ["ASR-903", "CISCO2811", "N7K-C7018"]
):
    print(
        f"Suggestion for {item.product.product_name} "
        f"({item.product.base_pid})..."
    )
    for suggestion in item.suggestions:
        print(f"- {suggestion.rel_display_name}")
    print("\n")


# find compatable software for product
for item in cs.suggestion.get_compatible_by_product_id("ASR-903"):
    print(item)

# get the suggested realease and image by MDF
for item in cs.suggestion.get_suggestions_and_image_by_mdf_ids(
    ["283933147", "283780951"]
):
    print(item)

# get the suggested realease and image by MDF
for item in cs.suggestion.get_suggestions_by_mdf_ids(
    ["283933147", "283780951"]
):
    print(item)

# find compatable software for product
for item in cs.suggestion.get_compatible_by_mdf_id("283933147"):
    print(item)
