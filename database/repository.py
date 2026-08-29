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