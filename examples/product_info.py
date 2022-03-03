import os

from ciscosupportsdk.api import CiscoSupportAPI

CS_API_KEY = os.getenv("CS_API_KEY")
CS_API_SECRET = os.getenv("CS_API_SECRET")

cs = CiscoSupportAPI(CS_API_KEY, CS_API_SECRET)

for item in cs.product_information.get_info_by_serial(
    ["SPE181700LN", "REF_CSJ07306405"]
):
    print(item.product_name)

for item in cs.product_information.get_info_by_product_id(
    ["UBR10012", "ASR1001"]
):
    print(item.product_name)

for item in cs.product_information.get_mdf_by_product_id(
    ["ASA5505-50-BUN-K9"]
):
    print(item.product_name_mdf)
