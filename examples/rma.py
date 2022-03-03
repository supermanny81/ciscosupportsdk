import os

from ciscosupportsdk.api import CiscoSupportAPI

CS_API_KEY = os.getenv("CS_API_KEY")
CS_API_SECRET = os.getenv("CS_API_SECRET")

cs = CiscoSupportAPI(CS_API_KEY, CS_API_SECRET)

for rma in cs.rma.get_rma_details_by_rma_number("801934965"):
    print(rma.case_id)

for rma in cs.rma.get_rma_details_by_user_id("mannygar"):
    print(rma.case_id)
