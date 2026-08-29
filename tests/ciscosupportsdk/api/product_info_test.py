"""
The Product Information API had no test coverage while the suite depended on
recorded traffic. These fixtures are built from the documented response
schema.
"""

import pytest

from fixtures import *  # noqa

BY_SERIAL = {
    "pagination_response_record": {
        "last_index": 1,
        "page_index": 1,
        "page_records": 1,
        "total_records": 1,
        "title": "Product Information API",
        "self_link": "https://apix.cisco.com/product/v1/information",
    },
    "product_list": [
        {
            "id": "1",
            "sr_no": "SAL1234ABCD",
            "base_pid": "WS-C3560-48PS-S",
            "orderable_pid": "WS-C3560-48PS-S=",
            "product_name": "Catalyst 3560 48 10/100 PoE + 4 SFP",
            "product_type": "Switches",
            "product_series": "Cisco Catalyst 3560 Series Switches",
            "product_category": "Switches",
            "product_subcategory": "Fixed Configuration Switches",
            "release_date": "2005-03-01",
            "orderable_status": "Not Orderable",
            "dimensions": {
                "dimensions_format": "H x W x D",
                "dimensions_value": "1.73 x 17.5 x 11.8 in",
            },
            "weight": "10.0 lb",
            "form_factor": "Fixed",
            "product_support_page": "https://www.cisco.com/c/en/us/support",
            "visio_stencil_url": "https://www.cisco.com/stencil.vss",
            "rich_media_urls": {
                "large_image_url": "https://www.cisco.com/large.jpg",
                "small_image_url": "https://www.cisco.com/small.jpg",
            },
        }
    ],
}

MDF = {
    "product_list": [
        {
            "id": "1",
            "product_id": "WS-C3560-48PS-S",
            "product_name": "Catalyst 3560 48 10/100 PoE + 4 SFP",
            "product_name_mdf": "Cisco Catalyst 3560-48PS Switch",
            "product_series": "Cisco Catalyst 3560 Series Switches",
            "product_series_mdf": "Cisco Catalyst 3560 Series Switches",
        }
    ]
}


class TestProductInformationApi:
    def test_get_info_by_serial(self, api_factory):
        api, client = api_factory(BY_SERIAL)

        record = next(
            api.product_information.get_info_by_serial(["SAL1234ABCD"])
        )

        # These three used to be dropped by the model entirely; sr_no is the
        # only way to tie a record back to the serial that was queried.
        assert record.sr_no == "SAL1234ABCD"
        assert record.base_pid == "WS-C3560-48PS-S"
        assert record.orderable_pid == "WS-C3560-48PS-S="
        assert record.dimensions.dimensions_value.startswith("1.73")
        assert "/product/v1/information/serial_numbers/" in client.urls[0]

    def test_get_info_by_product_id(self, api_factory):
        api, client = api_factory(BY_SERIAL)

        record = next(
            api.product_information.get_info_by_product_id(["WS-C3560-48PS-S"])
        )

        assert record.product_series
        assert "/product_ids/WS-C3560-48PS-S" in client.urls[0]

    def test_get_mdf_by_product_id(self, api_factory):
        api, client = api_factory(MDF)

        record = next(
            api.product_information.get_mdf_by_product_id(["WS-C3560-48PS-S"])
        )

        assert record.product_name_mdf == "Cisco Catalyst 3560-48PS Switch"
        assert "/product_ids_mdf/WS-C3560-48PS-S" in client.urls[0]

    def test_sparse_record(self, api_factory):
        # Release 1.0 only covers hardware and omits what it cannot fill in.
        api, _ = api_factory({"product_list": [{"id": "1", "sr_no": "X"}]})

        record = next(api.product_information.get_info_by_serial(["X"]))

        assert record.sr_no == "X"
        assert record.dimensions is None
        assert record.rich_media_urls is None

    def test_too_many_serials_is_rejected(self, api):
        # The documented maximum is five per call.
        with pytest.raises(ValueError, match="serial_numbers"):
            next(api.product_information.get_info_by_serial(["A"] * 6))
