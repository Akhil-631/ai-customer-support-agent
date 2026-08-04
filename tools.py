from database.repository import (
    get_order,
    cancel_order as db_cancel_order,
    get_refund,
    create_support_ticket
)

def cancel_order(order_id):

    rows_updated = db_cancel_order(order_id)

    if rows_updated == 0:
        return "Order not found."

    return (
        f"Order {order_id} has been cancelled successfully.\n"
        "Your refund will be processed within 5-7 business days."
    )

def get_delivery_status(order_id):

    result = get_order(order_id)

    if result is None:
        return "Order not found."

    return (
        f"Delivery Status: {result['delivery_status']}\n"
        f"Expected Delivery: {result['expected_delivery']}"
    )

def get_refund_status(order_id):

    refund = get_refund(order_id)

    if refund is None:
        return "No refund found for this order."

    return (
        f"Refund Status: {refund['refund_status']}\n"
        f"Refund Amount: ₹{refund['refund_amount']:.2f}\n"
        f"Reason: {refund['refund_reason']}\n"
        f"Refund Date: {refund['refund_date']}"
    )

def escalate_to_human(order_id, issue):

    ticket_id = create_support_ticket(
        order_id,
        issue
    )

    return (
        f"Your request requires human assistance.\n\n"
        f"Support Ticket ID : {ticket_id}\n"
        f"Assigned Team : Support Team\n"
        f"Priority : High\n"
        f"Status : Open"
    )

def get_order_status(order_id):

    result = get_order(order_id)

    if result is None:
        return "Order not found."

    return (
        f"Order Status: {result['order_status']}\n"
        f"Delivery Status: {result['delivery_status']}\n"
        f"Expected Delivery: {result['expected_delivery']}"
    )
