import os

from ciscosupportsdk.api import CiscoSupportAPI

CS_API_KEY = os.getenv("CS_API_KEY")
CS_API_SECRET = os.getenv("CS_API_SECRET")

cs = CiscoSupportAPI(CS_API_KEY, CS_API_SECRET)

# find if a serial number is covered and when it's warranty expires
for item in cs.serial_information.get_coverage_status(["FXS2130Q286"]):
    print(f"{item.is_covered} {item.coverage_end_date}")

# find if a serial number is covered and when it's contract expires
for item in cs.serial_information.get_coverage_summary_by_serial(
    ["FXS2130Q286"]
):
    print(item)

# find if a serial number is covered and when it's contract expires
for item in cs.serial_information.get_coverage_summary_by_instance(
    ["917280220"]
):
    print(item)

# find if a serial number is covered and when it's contract expires
for item in cs.serial_information.get_orderable_pids(["FXS2130Q286"]):
    print(item)

# find if a serial number is covered and when it's contract expires
for item in cs.serial_information.get_coverage_owner_status(["FXS2130Q286"]):
    print(item)
