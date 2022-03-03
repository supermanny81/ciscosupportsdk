import os

from ciscosupportsdk.api import CiscoSupportAPI
from ciscosupportsdk.models.bug import SortBy

CS_API_KEY = os.getenv("CS_API_KEY")
CS_API_SECRET = os.getenv("CS_API_SECRET")

cs = CiscoSupportAPI(CS_API_KEY, CS_API_SECRET)

for bug in cs.bug.get_bug_details(["CSCvc57217"]):
    print(f"{bug.bug_id}: {bug.headline}")

for bug in cs.bug.get_bugs_by_product_id(
    "WS-C3560-48PS-S", sort_by=SortBy.SEVERITY
):
    print(f"{bug.bug_id}: {bug.headline} {bug.known_affected_releases}")

for bug in cs.bug.get_bugs_by_product_id_and_release(
    "WS-C3560-48PS-S", ["15.2(03)E01"]
):
    print(f"{bug.bug_id}: {bug.headline}")

for bug in cs.bug.get_bugs_by_keyword("IOS SSH PKI"):
    print(f"{bug.bug_id}: {bug.headline}")
