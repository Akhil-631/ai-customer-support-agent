from database.repository import (
    get_order_lines,
    cancel_order as db_cancel_order,
    get_refund,
    create_support_ticket
)

from models import ToolResult

def get_order_lines_data(order_id):

    lines = get_order_lines(order_id)

    if lines is None:
        return None

    return lines


def get_order_status(order_id):

    lines = get_order_lines_data(order_id)

    if lines is None:

        return ToolResult(
            success=False,
            message="Order not found.",
            error="ORDER_NOT_FOUND"
        )

    order_statuses = {
        line["order_status"]
        for line in lines
    }

    delivery_statuses = {
        line["delivery_status"]
        for line in lines
    }

    expected_deliveries = [
        line["expected_delivery"]
        for line in lines
    ]

    if len(order_statuses) == 1:
        overall_order_status = next(iter(order_statuses))
    else:
        overall_order_status = "Mixed"

    if len(delivery_statuses) == 1:
        overall_delivery_status = next(iter(delivery_statuses))
    else:
        overall_delivery_status = "Mixed"

    expected_delivery = max(expected_deliveries)

    return ToolResult(
        success=True,
        message="Order status retrieved successfully.",
        data={
            "order_id": order_id,
            "order_status": overall_order_status,
            "delivery_status": overall_delivery_status,
            "expected_delivery": expected_delivery
        }
    )


def get_delivery_status(order_id):

    lines = get_order_lines_data(order_id)

    if lines is None:

        return ToolResult(
            success=False,
            message="Order not found.",
            error="ORDER_NOT_FOUND"
        )

    delivery_statuses = {
        line["delivery_status"]
        for line in lines
    }

    expected_deliveries = [
        line["expected_delivery"]
        for line in lines
    ]

    if len(delivery_statuses) == 1:
        overall_delivery_status = next(iter(delivery_statuses))
    else:
        overall_delivery_status = "Mixed"

    expected_delivery = max(expected_deliveries)

    return ToolResult(
        success=True,
        message="Delivery status retrieved successfully.",
        data={
            "order_id": order_id,
            "delivery_status": overall_delivery_status,
            "expected_delivery": expected_delivery
        }
    )


def cancel_order(order_id):

    lines = get_order_lines_data(order_id)

    if lines is None:

        return ToolResult(
            success=False,
            message="Order not found.",
            error="ORDER_NOT_FOUND"
        )

    order_statuses = {
        line["order_status"]
        for line in lines
    }

    delivery_statuses = {
        line["delivery_status"]
        for line in lines
    }

    # Already cancelled
    if order_statuses == {"Cancelled"}:

        return ToolResult(
            success=False,
            message=f"Order {order_id} is already cancelled.",
            error="ORDER_ALREADY_CANCELLED"
        )

    # Delivered items cannot be cancelled
    if "Delivered" in delivery_statuses:

        return ToolResult(
            success=False,
            message=(
                f"Order {order_id} cannot be cancelled because "
                "one or more items have already been delivered."
            ),
            error="ORDER_NOT_CANCELLABLE"
        )

    # Mixed fulfillment states require human review
    if len(order_statuses) > 1 or len(delivery_statuses) > 1:

        return ToolResult(
            success=False,
            message=(
                f"Order {order_id} has multiple fulfillment states "
                "and requires human assistance before it can be cancelled."
            ),
            error="MIXED_FULFILLMENT_STATE"
        )

    rows_updated = db_cancel_order(order_id)

    if rows_updated == 0:

        return ToolResult(
            success=False,
            message="Order could not be cancelled.",
            error="CANCELLATION_FAILED"
        )

    return ToolResult(
        success=True,
        message=(
            f"Order {order_id} has been cancelled successfully. "
            "Your refund will be processed within 5-7 business days."
        ),
        data={
            "order_id": order_id,
            "rows_updated": rows_updated,
            "refund_processing_time": "5-7 business days"
        }
    )

def get_refund_status(order_id):

    refund = get_refund(order_id)

    if refund is None:

        return ToolResult(
            success=False,
            message="No refund found for this order.",
            error="REFUND_NOT_FOUND"
        )

    return ToolResult(
        success=True,
        message="Refund status retrieved successfully.",
        data={
            "order_id": order_id,
            "refund_status": refund["refund_status"],
            "refund_amount": refund["refund_amount"],
            "refund_reason": refund["refund_reason"],
            "refund_date": refund["refund_date"]
        }
    )

def escalate_to_human(order_id, issue):

    ticket_id = create_support_ticket(
        order_id,
        issue
    )

    return ToolResult(
        success=True,
        message="Your request has been escalated to human support.",
        data={
            "ticket_id": ticket_id,
            "order_id": order_id,
            "assigned_team": "Support Team",
            "priority": "High",
            "status": "Open"
        }
    )

