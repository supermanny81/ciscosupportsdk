from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field

from .common import CamelCaseApi, PaginationResponseRecord

# RMA payloads are heavily state dependent: labor details only exist for onsite
# service, tracking information only appears once a part has shipped, return
# lines only once a part is coming back, and address blocks are frequently
# partial. Every field therefore carries a default so that validation never
# fails on a well-formed but sparse response.


class CustomerRefInfo(BaseModel):
    customer_po_number: Optional[str] = Field(None, alias="customerPONumber")
    orig_sales_order_number: Optional[str] = Field(
        None, alias="origSalesOrderNumber"
    )
    customer_ref_number: Optional[str] = Field(None, alias="customerRefNumber")
    customer_provided_sn: Optional[str] = Field(
        None, alias="customerProvidedSN"
    )


class ShipToInfo(BaseModel):
    customer_name: Optional[str] = Field(None, alias="customerName")
    address1: Optional[str] = None
    address2: Optional[str] = None
    address3: Optional[str] = None
    address4: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    postal_code: Optional[str] = Field(None, alias="postalCode")
    state_prov: Optional[str] = Field(None, alias="stateProv")
    site_use_id: Optional[str] = Field(None, alias="siteUseId")
    ack_user_id: Optional[str] = Field(None, alias="ackUserId")
    ack_phone: Optional[str] = Field(None, alias="ackPhone")
    ack_email: Optional[str] = Field(None, alias="ackEmail")
    ack_name: Optional[str] = Field(None, alias="ackName")
    ship_to_contact_name: Optional[str] = Field(
        None, alias="shipToContactName"
    )
    ship_to_contact_phone: Optional[str] = Field(
        None, alias="shipToContactPhone"
    )
    ship_to_contact_email: Optional[str] = Field(
        None, alias="shipToContactEmail"
    )


class BillToInfo(BaseModel):
    customer_name: Optional[str] = Field(None, alias="customerName")
    address1: Optional[str] = None
    address2: Optional[str] = None
    address3: Optional[str] = None
    address4: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    postal_code: Optional[str] = Field(None, alias="postalCode")
    state_prov: Optional[str] = Field(None, alias="stateProv")
    site_use_id: Optional[str] = Field(None, alias="siteUseId")


class TrackingInfo(BaseModel):
    tracking_number: Optional[str] = Field(None, alias="trackingNumber")
    courier_list: Optional[str] = Field(None, alias="courierList")
    ship_date: Optional[str] = Field(None, alias="shipDate")


class PartsLineDetail(BaseModel):
    parts_line_ref: Optional[str] = Field(None, alias="partsLineRef")
    parts_line_status: Optional[str] = Field(None, alias="partsLineStatus")
    parts_transaction_type: Optional[str] = Field(
        None, alias="partsTransactionType"
    )
    shipped_part_no: Optional[str] = Field(None, alias="shippedPartNo")
    parts_description: Optional[str] = Field(None, alias="partsDescription")
    parts_qty_auth: Optional[str] = Field(None, alias="partsQtyAuth")
    parts_scheduled_ship_time: Optional[str] = Field(
        None, alias="partsScheduledShipTime"
    )
    partsqty_shipped: Optional[str] = Field(None, alias="partsqtyShipped")
    parts_ship_date: Optional[str] = Field(None, alias="partsShipDate")
    parts_shipment_warehouse: Optional[str] = Field(
        None, alias="partsShipmentWarehouse"
    )
    parts_dispatch_status: Optional[str] = Field(
        None, alias="partsDispatchStatus"
    )


class ReplacementParts(BaseModel):
    tracking_info: Optional[TrackingInfo] = Field(None, alias="trackingInfo")
    parts_line_details: List[PartsLineDetail] = Field(
        default_factory=list, alias="partsLineDetails"
    )


class ReturnPart(BaseModel):
    return_line_ref: Optional[str] = Field(None, alias="returnLineRef")
    return_line_status: Optional[str] = Field(None, alias="returnLineStatus")
    return_transaction_type: Optional[str] = Field(
        None, alias="returnTransactionType"
    )
    received_part_no: Optional[str] = Field(None, alias="receivedPartNo")
    return_description: Optional[str] = Field(None, alias="returnDescription")
    return_qty_auth: Optional[str] = Field(None, alias="returnQtyAuth")
    return_to_cisco_by: Optional[str] = Field(None, alias="returnToCiscoBy")
    reqturn_qty_received: Optional[str] = Field(
        None, alias="reqturnQtyReceived"
    )
    return_date_received: Optional[str] = Field(
        None, alias="returnDateReceived"
    )
    return_warehouse: Optional[str] = Field(None, alias="returnWarehouse")


class ReturnLines(BaseModel):
    return_parts: List[ReturnPart] = Field(
        default_factory=list, alias="returnParts"
    )


class LaborLine(BaseModel):
    labor_task_number: Optional[str] = Field(None, alias="laborTaskNumber")
    labor_status: Optional[str] = Field(None, alias="laborStatus")
    primary_product_family: Optional[str] = Field(
        None, alias="primaryProductFamily"
    )
    labor_scheduled_time: Optional[str] = Field(
        None, alias="laborScheduledTime"
    )
    labor_dispatch: Optional[str] = Field(None, alias="laborDispatch")
    labor_dispatch_or_cancellation_notes: Optional[str] = Field(
        None, alias="laborDispatchOrCancellationNotes"
    )


class LaborDetails(BaseModel):
    field_engineer_name: Optional[str] = Field(None, alias="fieldEngineerName")
    field_engineer_phone: Optional[str] = Field(
        None, alias="fieldEngineerPhone"
    )
    field_engineer_on_route_time: Optional[str] = Field(
        None, alias="fieldEngineerOnRouteTime"
    )
    field_engineer_arrived_time: Optional[str] = Field(
        None, alias="fieldEngineerArrivedTime"
    )
    field_engineer_released_time: Optional[str] = Field(
        None, alias="fieldEngineerReleasedTime"
    )
    labor_lines: List[LaborLine] = Field(
        default_factory=list, alias="laborLines"
    )


class Notes(BaseModel):
    addl_comments: Optional[str] = Field(None, alias="addlComments")
    failure_description: Optional[str] = Field(
        None, alias="failureDescription"
    )
    field_engineer_instructions: Optional[str] = Field(
        None, alias="fieldEngineerInstructions"
    )
    part_delivery_instructions: Optional[str] = Field(
        None, alias="partDeliveryInstructions"
    )
    partial_shipment_note: Optional[str] = Field(
        None, alias="partialShipmentNote"
    )
    special_instructions: Optional[str] = Field(
        None, alias="specialInstructions"
    )


class ShippingAddress(BaseModel):
    """Address block returned by the RMAs-by-user-id endpoint."""

    customer_name: Optional[str] = Field(None, alias="customerName")
    address1: Optional[str] = None
    address2: Optional[str] = None
    address3: Optional[str] = None
    address4: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    postal_code: Optional[str] = Field(None, alias="postalCode")
    state_prov: Optional[str] = Field(None, alias="stateProv")
    site_use_id: Optional[str] = Field(None, alias="siteUseId")


class Rma(BaseModel):
    rma_no: Optional[int] = Field(None, alias="rmaNo")
    status: Optional[str] = None
    order_date: Optional[str] = Field(None, alias="orderDate")
    case_id: Optional[str] = Field(None, alias="caseId")
    requested_ship_date: Optional[str] = Field(None, alias="requestedShipDate")
    originator: Optional[str] = None
    allow_partial_shipment: Optional[str] = Field(
        None, alias="allowPartialShipment"
    )
    failure_class: Optional[str] = Field(None, alias="failureClass")
    failure_code: Optional[str] = Field(None, alias="failureCode")
    contract_id: Optional[str] = Field(None, alias="contractId")
    service_level: Optional[str] = Field(None, alias="serviceLevel")
    customer_ref_info: Optional[CustomerRefInfo] = Field(
        None, alias="customerRefInfo"
    )
    ship_to_info: Optional[ShipToInfo] = Field(None, alias="shipToInfo")
    bill_to_info: Optional[BillToInfo] = Field(None, alias="billToInfo")
    replacement_parts: Optional[ReplacementParts] = Field(
        None, alias="replacementParts"
    )
    return_lines: Optional[ReturnLines] = Field(None, alias="returnLines")
    labor_details: Optional[LaborDetails] = Field(None, alias="laborDetails")
    notes: Optional[Notes] = None
    # Fields specific to the RMAs-by-user-id summary view.
    ordered_part: Optional[str] = Field(None, alias="orderedPart")
    customer_provided_sn: Optional[str] = Field(
        None, alias="customerProvidedSN"
    )
    courier_list: Optional[str] = Field(None, alias="courierList")
    earliest_ship_date_time: Optional[str] = Field(
        None, alias="earliestShipDateTime"
    )
    on_site_contact_name: Optional[str] = Field(
        None, alias="onSiteContactName"
    )
    on_site_contact_phone: Optional[str] = Field(
        None, alias="onSiteContactPhone"
    )
    on_site_contact_email: Optional[str] = Field(
        None, alias="onSiteContactEmail"
    )
    shipping_address: Optional[ShippingAddress] = Field(
        None, alias="shippingAddress"
    )


class Returns(BaseModel):
    rma_records: List[Rma] = Field(default_factory=list, alias="RmaRecord")


class RmaResponse(BaseModel, CamelCaseApi):
    pagination_response_record: Optional[PaginationResponseRecord] = Field(
        None, alias="APIPagination"
    )
    items: Returns = Field(default_factory=Returns, alias="returns")


class User(BaseModel):
    user_id: Optional[str] = Field(None, alias="userId")
    return_count: Optional[str] = Field(None, alias="returnCount")
    returns: List[Rma] = Field(default_factory=list)


class OrderList(BaseModel):
    pagination_response_record: Optional[PaginationResponseRecord] = Field(
        None, alias="APIPagination"
    )
    users: List[User] = Field(default_factory=list)


class RmaByUserResponse(BaseModel):
    order_list: OrderList = Field(..., alias="OrderList")
