ciscosupportsdk examples
========================

The files in this folder serve as examples for using all parts of the cisco support sdk.

Some requirements on usage
--------------------------
 .. code-block:: Python

    CS_API_KEY = os.getenv("CS_API_KEY")
    CS_API_SECRET = os.getenv("CS_API_SECRET")


 In order to run them, you will need to have ``ciscosupportsdk`` installed 
 or available in your path as well as a validate key and token as an environment variable.
 If you don not have client key and token see the `support api`_ documentation for more
 information.

 In addition, some extra information may need to be passed before getting favorable
 results.  Some APIs like ``eox`` and ``software_suggestion`` are not customer specific, while
 others like ``case`` will require replacing paramters passed to ones that are customer
 specific.

.. _support api: https://developer.cisco.com/docs/support-apis/