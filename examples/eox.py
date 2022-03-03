import os

from ciscosupportsdk.api import CiscoSupportAPI
from ciscosupportsdk.models.eox import EoxAttrib, OSType, SoftwareRelease

CS_API_KEY = os.getenv("CS_API_KEY")
CS_API_SECRET = os.getenv("CS_API_SECRET")

cs = CiscoSupportAPI(CS_API_KEY, CS_API_SECRET)

# get a list of things that went end of support in January 20200
for eox_item in cs.eox.get_by_dates(
    "2022-01-01", "2022-01-31", [EoxAttrib.EO_LAST_SUPPORT_DATE]
):

    print(f"{eox_item.eol_product_id} {eox_item.end_of_sale_date}")

# find EoX by product IDs
for e in cs.eox.get_by_product_ids(["MR42*"]):
    print(
        f"{e.eol_product_id}: sale: {e.end_of_sale_date.value} support:{e.last_date_of_support.value}"
    )

# get EoX record for a serial number
for eox_item in cs.eox.get_by_serial_number(["Q2KD-BJDU-R26R"]):
    print(eox_item.eol_product_id)

# find what product ids by software release are EoX
for eox_item in cs.eox.get_by_software_release(
    [SoftwareRelease(os=OSType.IOS, version="12.2")]
):
    print(f"{eox_item.eol_product_id} {eox_item.product_id_description}")
