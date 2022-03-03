from __future__ import annotations

from typing import List

from pydantic import BaseModel, Field

from .common import CamelCaseApi, PaginationResponseRecord


class CustomerRefInfo(BaseModel):
    customer_po_number: str = Field(..., alias="customerPONumber")
    orig_sales_order_number: str = Field(..., alias="origSalesOrderNumber")
    customer_ref_number: str = Field(..., alias="customerRefNumber")
    customer_provided_sn: str = Field(..., alias="customerProvidedSN")


class ShipToInfo(BaseModel):
    customer_name: str = Field(..., alias="customerName")
    address1: str
    address2: str
    address3: str
    address4: str
    city: str
    state: str
    country: str
    postal_code: str = Field(..., alias="postalCode")
    state_prov: str = Field(..., alias="stateProv")
    site_use_id: str = Field(..., alias="siteUseId")
    ack_user_id: str = Field(..., alias="ackUserId")
    ack_phone: str = Field(..., alias="ackPhone")
    ack_email: str = Field(..., alias="ackEmail")
    ack_name: str = Field(..., alias="ackName")
    ship_to_contact_name: str = Field(..., alias="shipToContactName")
    ship_to_contact_phone: str = Field(..., alias="shipToContactPhone")
    ship_to_contact_email: str = Field(..., alias="shipToContactEmail")


class BillToInfo(BaseModel):
    customer_name: str = Field(..., alias="customerName")
    address1: str
    address2: str
    address3: str
    address4: str
    city: str
    state: str
    country: str
    postal_code: str = Field(..., alias="postalCode")
    state_prov: str = Field(..., alias="stateProv")
    site_use_id: str = Field(..., alias="siteUseId")


class TrackingInfo(BaseModel):
    tracking_number: str = Field(..., alias="trackingNumber")
    courier_list: str = Field(..., alias="courierList")
    ship_date: str = Field(..., alias="shipDate")


class PartsLineDetail(BaseModel):
    parts_line_ref: str = Field(..., alias="partsLineRef")
    parts_line_status: str = Field(..., alias="partsLineStatus")
    parts_transaction_type: str = Field(..., alias="partsTransactionType")
    shipped_part_no: str = Field(..., alias="shippedPartNo")
    parts_description: str = Field(..., alias="partsDescription")
    parts_qty_auth: str = Field(..., alias="partsQtyAuth")
    parts_scheduled_ship_time: str = Field(..., alias="partsScheduledShipTime")
    partsqty_shipped: str = Field(..., alias="partsqtyShipped")
    parts_ship_date: str = Field(..., alias="partsShipDate")
    parts_shipment_warehouse: str = Field(..., alias="partsShipmentWarehouse")
    parts_dispatch_status: str = Field(..., alias="partsDispatchStatus")


class ReplacementParts(BaseModel):
    tracking_info: TrackingInfo = Field(..., alias="trackingInfo")
    parts_line_details: List[PartsLineDetail] = Field(
        ..., alias="partsLineDetails"
    )


class ReturnPart(BaseModel):
    return_line_ref: str = Field(..., alias="returnLineRef")
    return_line_status: str = Field(..., alias="returnLineStatus")
    return_transaction_type: str = Field(..., alias="returnTransactionType")
    received_part_no: str = Field(..., alias="receivedPartNo")
    return_description: str = Field(..., alias="returnDescription")
    return_qty_auth: str = Field(..., alias="returnQtyAuth")
    return_to_cisco_by: str = Field(..., alias="returnToCiscoBy")
    reqturn_qty_received: str = Field(..., alias="reqturnQtyReceived")
    return_date_received: str = Field(..., alias="returnDateReceived")
    return_warehouse: str = Field(..., alias="returnWarehouse")


class ReturnLines(BaseModel):
    return_parts: List[ReturnPart] = Field(..., alias="returnParts")


class LaborLine(BaseModel):
    labor_task_number: str = Field(..., alias="laborTaskNumber")
    labor_status: str = Field(..., alias="laborStatus")
    primary_product_family: str = Field(..., alias="primaryProductFamily")
    labor_scheduled_time: str = Field(..., alias="laborScheduledTime")
    labor_dispatch: str = Field(..., alias="laborDispatch")
    labor_dispatch_or_cancellation_notes: str = Field(
        ..., alias="laborDispatchOrCancellationNotes"
    )


class LaborDetails(BaseModel):
    field_engineer_name: str = Field(..., alias="fieldEngineerName")
    field_engineer_phone: str = Field(..., alias="fieldEngineerPhone")
    field_engineer_on_route_time: str = Field(
        ..., alias="fieldEngineerOnRouteTime"
    )
    field_engineer_arrived_time: str = Field(
        ..., alias="fieldEngineerArrivedTime"
    )
    field_engineer_released_time: str = Field(
        ..., alias="fieldEngineerReleasedTime"
    )
    labor_lines: List[LaborLine] = Field(..., alias="laborLines")


class Notes(BaseModel):
    addl_comments: str = Field(..., alias="addlComments")
    failure_description: str = Field(..., alias="failureDescription")
    field_engineer_instructions: str = Field(
        ..., alias="fieldEngineerInstructions"
    )
    part_delivery_instructions: str = Field(
        ..., alias="partDeliveryInstructions"
    )
    partial_shipment_note: str = Field(..., alias="partialShipmentNote")
    special_instructions: str = Field(..., alias="specialInstructions")


class Rma(BaseModel):
    rma_no: int = Field(..., alias="rmaNo")
    status: str
    order_date: str = Field(..., alias="orderDate")
    case_id: str = Field(..., alias="caseId")
    requested_ship_date: str = Field(..., alias="requestedShipDate")
    originator: str
    allow_partial_shipment: str = Field(..., alias="allowPartialShipment")
    failure_class: str = Field(..., alias="failureClass")
    failure_code: str = Field(..., alias="failureCode")
    contract_id: str = Field(..., alias="contractId")
    service_level: str = Field(..., alias="serviceLevel")
    customer_ref_info: CustomerRefInfo = Field(..., alias="customerRefInfo")
    ship_to_info: ShipToInfo = Field(..., alias="shipToInfo")
    bill_to_info: BillToInfo = Field(..., alias="billToInfo")
    replacement_parts: ReplacementParts = Field(..., alias="replacementParts")
    return_lines: ReturnLines = Field(..., alias="returnLines")
    labor_details: LaborDetails = Field(..., alias="laborDetails")
    notes: Notes


class Returns(BaseModel):
    rma_records: List[Rma] = Field(..., alias="RmaRecord")


class RmaResponse(BaseModel, CamelCaseApi):
    pagination_response_record: PaginationResponseRecord = Field(
        ..., alias="APIPagination"
    )
    items: Returns = Field(..., alias="returns")


class User(BaseModel):
    user_id: str = Field(..., alias="userId")
    return_count: str = Field(..., alias="returnCount")
    returns: List[Rma]


class OrderList(BaseModel):
    pagination_response_record: PaginationResponseRecord = Field(
        ..., alias="APIPagination"
    )
    users: List[User]


class RmaByUserResponse(BaseModel):
    order_list: OrderList = Field(..., alias="OrderList")
