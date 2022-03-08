ciscosupportsdk
===============

Python API wrapper for the Cisco Support APIs.

|devnet| |docs| |tests| |coverage| |pypi|

----------------------------------------------

The **ciscosupportsdk** supports all of the Cisco Support API
interactions via a native Python library.  This makes working with
these APIs a more *natural* experience and eases the burden of writing
your own boilerplate code to deal with API semantics, like authentication
and pagination.

For detailed information and onboarding information, see the `support api`_
documentation on DevNet. 

Quick Usage
-----------
.. code-block:: Python

   from ciscosupportsdk.api import CiscoSupportAPI

   api = CiscoSupportAPI(CS_API_KEY, CS_API_SECRET)

   # find if a serial number is covered and when it's warranty expires
   for item in api.serial_information.get_coverage_status(['FXS2130Q286']):
      print(f'{item.is_covered} {item.warranty_end_date}')


The User Guide
--------------
.. toctree::
   :maxdepth: 4

   intro.rst
   api/ciscosupportsdk.rst



Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


.. _support api: https://developer.cisco.com/docs/support-apis/
.. |docs| image:: https://github.com/supermanny81/ciscosupportapi/actions/workflows/docs_to_pages.yaml/badge.svg 
   :target: https://github.com/supermanny81/ciscosupportapi/actions/workflows/docs_to_pages.yaml
.. |coverage| image:: https://codecov.io/gh/supermanny81/ciscosupportapi/branch/master/graph/badge.svg?token=CU4V95TVF1
   :target: https://codecov.io/gh/supermanny81/ciscosupportapi
.. |tests| image:: https://github.com/supermanny81/ciscosupportapi/actions/workflows/test.yaml/badge.svg
   :target: https://github.com/supermanny81/ciscosupportapi/actions/workflows/test.yaml
.. |pypi| image:: https://badge.fury.io/py/ciscosupportsdk.svg
   :target: https://badge.fury.io/py/ciscosupportsdk
.. |devnet| image:: https://static.production.devnetcloud.com/codeexchange/assets/images/devnet-published.svg
   :target: https://developer.cisco.com/codeexchange/github/repo/supermanny81/ciscosupportsdk
.. _examples: https://github.com/supermanny81/ciscosupportsdk/tree/master/examples