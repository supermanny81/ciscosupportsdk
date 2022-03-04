.. _Support API documentation:
.. currentmodule:: ciscosupportsdk

===========
API Details
===========

CiscoSupportAPI
===============
The :class:`CiscoSupportAPI` class creates "session objects" for wrapping support APIs.
Each support API endpoint is available to an instance of the `ciscosupportsdk`.
::

    from ciscosupportsdk.api import CiscoSupportAPI

    cs = CiscoSupportAPI(CS_API_KEY, CS_API_SECRET)

.. automodule:: ciscosupportsdk.api
    :members: 
    :show-inheritance:

asd
---

.. automodule:: ciscosupportsdk.api.asd
    :members: 
    :show-inheritance:


bug
-------
Used to makes calls to the ``BugApi`` endpoint.
    >>> cs = CiscoSupportAPI(CS_API_KEY, CS_API_SECRET)
    >>> cs.bug
    <ciscosupportsdk.api.bug.BugApi object at 0x10451eb20>

.. automodule:: ciscosupportsdk.api.bug
    :members: 
    :show-inheritance:

case
----
.. automodule:: ciscosupportsdk.api.case
    :members: 
    :show-inheritance:

eox
---
.. automodule:: ciscosupportsdk.api.eox
    :members: 
    :show-inheritance:

product_information
-------------------
.. automodule:: ciscosupportsdk.api.productinformation
    :members: 
    :show-inheritance:

serial_information
------------------
.. automodule:: ciscosupportsdk.api.serialnumbertoinformation
    :members: 
    :show-inheritance:

.. _serviceorderreturn:

serviceorderreturn
------------------
.. automodule:: ciscosupportsdk.api.serviceorderreturn
    :members: 
    :show-inheritance:

suggestion
-----------
.. automodule:: ciscosupportsdk.api.softwaresuggestion
    :members: 
    :show-inheritance:

rma
---
While known as an RMA to many customers and partners, the service endpoint here
is described above in :ref:`serviceorderreturn<serviceorderreturn>`.  This member is
here for convenience and references the same API endpoint.