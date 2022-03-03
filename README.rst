ciscosupportsdk
===============

Python API wrapper for the Cisco Support APIs.

----------------------------------------------

The **ciscosupportsdk** supports all of the Cisco Support API
interactions via a native Python library.  This makes working with
these APIs a more *natural* experience and eases the burden of writing
your own boilerplate code to deal with API semantics, like authentication
 and pagination.

Quick Usage
-----------
.. code-block:: Python

   from ciscosupportsdk.api import CiscoSupportAPI

   api = CiscoSupportAPI(CS_API_KEY, CS_API_SECRET)

   # find if a serial number is covered and when it's warranty expires
   for item in api.serial_information.get_coverage_status(['FXS2130Q286']):
      print(f'{item.is_covered} {item.warranty_end_date}')

