import os

from ciscosupportsdk.api import CiscoSupportAPI

CS_API_KEY = os.getenv('CS_API_KEY')
CS_API_SECRET = os.getenv('CS_API_SECRET')

cs = CiscoSupportAPI(CS_API_KEY, CS_API_SECRET)

print(cs.case.get_case_details('692277140'))

for case in cs.case.get_cases_by_contract_id(['92511831']):
    print(f'{case.case_id}')

for case in cs.case.get_cases_by_user_id(['whouse', 'anjs']):
    print(case)


# CSCvc57217