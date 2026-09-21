import os
import pandas as pd
from sqlalchemy import create_engine, text
from urllib.parse import quote_plus
from dotenv import load_dotenv

load_dotenv()

USERNAME = os.getenv("DB_USERNAME")
PASSWORD = quote_plus(os.getenv("DB_PASSWORD"))
HOST = os.getenv("DB_HOST")
PORT = os.getenv("DB_PORT")
DATABASE = os.getenv("DB_NAME")

engine = create_engine(
    f"postgresql+psycopg2://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"
)

def get_order(order_id):

    query = text("""
        SELECT
            order_status,
            delivery_status,
            expected_delivery
        FROM orders
        WHERE order_id = :order_id
        LIMIT 1;
    """)

    with engine.connect() as connection:
        result = connection.execute(query, {"order_id": order_id}).fetchone()

    if result is None:
        return None

    return {
        "order_status": result.order_status,
        "delivery_status": result.delivery_status,
        "expected_delivery": str(result.expected_delivery)
    }

def get_order_lines(order_id):

    query = text("""
        SELECT
            order_id,
            product_name,
            order_status,
            delivery_status,
            expected_delivery
        FROM orders
        WHERE order_id = :order_id
        ORDER BY id;
    """)

    with engine.connect() as connection:

        results = connection.execute(
            query,
            {"order_id": order_id}
        ).fetchall()

    if not results:
        return None

    return [
        {
            "order_id": row.order_id,
            "product_name": row.product_name,
            "order_status": row.order_status,
            "delivery_status": row.delivery_status,
            "expected_delivery": str(row.expected_delivery)
        }
        for row in results
    ]

def cancel_order(order_id):

    query = text("""
        UPDATE orders
        SET order_status = 'Cancelled'
        WHERE order_id = :order_id
    """)

    with engine.begin() as connection:
        result = connection.execute(
            query,
            {"order_id": order_id}
        )

    return result.rowcount

def get_refund(order_id):

    query = text("""
        SELECT
            refund_status,
            refund_amount,
            refund_reason,
            refund_date
        FROM refunds
        WHERE order_id = :order_id
        LIMIT 1;
    """)

    with engine.connect() as connection:
        result = connection.execute(
            query,
            {"order_id": order_id}
        ).fetchone()

    if result is None:
        return None

    return {
        "refund_status": result.refund_status,
        "refund_amount": float(result.refund_amount),
        "refund_reason": result.refund_reason,
        "refund_date": str(result.refund_date)
    }

def create_support_ticket(order_id, issue):

    query = text("""
        INSERT INTO support_tickets
        (
            order_id,
            customer_issue,
            priority,
            status,
            assigned_to
        )

        VALUES
        (
            :order_id,
            :issue,
            'High',
            'Open',
            'Support Team'
        )

        RETURNING ticket_id;
    """)

    with engine.begin() as connection:

        ticket = connection.execute(
            query,
            {
                "order_id": order_id,
                "issue": issue
            }
        ).fetchone()

    return ticket.ticket_id

def create_human_review(
    conversation_id,
    order_id,
    request_type,
    issue
):

    query = text("""
        INSERT INTO human_review_requests
        (
            conversation_id,
            order_id,
            request_type,
            issue,
            status
        )
        VALUES
        (
            :conversation_id,
            :order_id,
            :request_type,
            :issue,
            'Pending'
        )
        RETURNING review_id;
    """)

    with engine.begin() as connection:

        review = connection.execute(
            query,
            {
                "conversation_id": conversation_id,
                "order_id": order_id,
                "request_type": request_type,
                "issue": issue
            }
        ).fetchone()

    return review.review_id


def get_pending_human_reviews():

    query = text("""
        SELECT
            review_id,
            conversation_id,
            order_id,
            request_type,
            issue,
            status,
            created_at,
            updated_at
        FROM human_review_requests
        WHERE status = 'Pending'
        ORDER BY created_at ASC;
    """)

    with engine.connect() as connection:

        results = connection.execute(query).fetchall()

    return [
        {
            "review_id": row.review_id,
            "conversation_id": row.conversation_id,
            "order_id": row.order_id,
            "request_type": row.request_type,
            "issue": row.issue,
            "status": row.status,
            "created_at": str(row.created_at),
            "updated_at": str(row.updated_at)
        }
        for row in results
    ]


def update_human_review(review_id, status):

    query = text("""
        UPDATE human_review_requests
        SET
            status = :status,
            updated_at = CURRENT_TIMESTAMP
        WHERE review_id = :review_id;
    """)

    with engine.begin() as connection:

        result = connection.execute(
            query,
            {
                "review_id": review_id,
                "status": status
            }
        )

    return result.rowcount

def update_human_review_by_conversation(conversation_id, status):

    query = text("""
        UPDATE human_review_requests
        SET
            status = :status,
            updated_at = CURRENT_TIMESTAMP
        WHERE conversation_id = :conversation_id
          AND status = 'Pending';
    """)

    with engine.begin() as connection:

        result = connection.execute(
            query,
            {
                "conversation_id": conversation_id,
                "status": status
            }
        )

    return result.rowcount