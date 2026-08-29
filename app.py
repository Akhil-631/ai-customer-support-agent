import streamlit as st
import uuid
import requests


st.set_page_config(
    page_title="Enterprise AI Customer Support Agent",
    page_icon="🤖",
    layout="wide"
)

if "conversation_id" not in st.session_state:
    st.session_state["conversation_id"] = str(uuid.uuid4())

st.sidebar.caption(
    f"Conversation ID: {st.session_state['conversation_id']}"
)

st.info(
    "This AI Agent classifies customer intent, selects the appropriate business tool, retrieves live data from PostgreSQL, and escalates complex requests to human support when required."
)

with st.sidebar:

    st.title("💡 Example Queries")

    st.write("📦 What is the status of order CA-2017-152156?")

    st.write("🚚 Where is my order CA-2017-152156?")

    st.write("💰 What is the refund status of order CA-2017-152156?")

    st.write("❌ Cancel my order CA-2017-152156")

    st.write("💳 My payment was deducted twice.")

st.title("🤖 Enterprise AI Customer Support Agent")

st.markdown("""
### Enterprise-ready AI Agent demonstrating:

- 🧠 Intent Classification using LLM
- 🛠️ Tool Calling Architecture
- 🗄️ PostgreSQL Integration
- 👨‍💼 Human-in-the-Loop Workflow

Ask anything about your orders, deliveries, refunds or customer support.
""")

user_query = st.text_input(
    "Enter your query"
)

if st.button("Submit"):

    if user_query.strip() == "":

        st.warning("Please enter a customer support query to continue.")

    else:

        with st.spinner("🤖 AI Agent is analyzing your request..."):

            response = requests.post(
                "http://127.0.0.1:8000/chat",
                json={
                    "message": user_query,
                    "conversation_id": st.session_state["conversation_id"]
                }
            )

            response.raise_for_status()

            result = response.json()

            st.session_state["result"] = result

        st.rerun()

        st.divider()

if "result" in st.session_state:

    result = st.session_state["result"]

    # --------------------------------
    # Human Review
    # --------------------------------

    if result.get("human_review_required", False):

        st.warning(
            "⚠️ Human Review Required"
        )

        review_data = result.get(
            "human_review_data"
        )

        if review_data:

            st.write(
                "**Customer Query:**",
                review_data.get(
                    "user_query",
                    "-"
                )
            )

            st.write(
                "**Intent:**",
                review_data.get(
                    "intent",
                    "-"
                )
            )

            st.write(
                "**Order ID:**",
                review_data.get(
                    "order_id",
                    "-"
                )
            )

        st.divider()

        st.subheader(
            "👨‍💼 Human Decision"
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            approve = st.button(
                "✅ Approve & Execute",
                use_container_width=True
            )

        with col2:

            reject = st.button(
                "❌ Reject",
                use_container_width=True
            )

        with col3:

            escalate = st.button(
                "👨‍💼 Escalate",
                use_container_width=True
            )

        decision = None

        if approve:
            decision = "approve"

        elif reject:
            decision = "reject"

        elif escalate:
            decision = "escalate"

        if decision:

            with st.spinner(
                "Processing human decision..."
            ):

                review_response = requests.post(
                    "http://127.0.0.1:8000/human-review",
                    json={
                        "conversation_id":
                            st.session_state[
                                "conversation_id"
                            ],
                        "decision": decision
                    }
                )

                review_response.raise_for_status()

                result = review_response.json()

                st.session_state["result"] = result

            st.rerun()

    st.subheader("🧠 Agent Response")

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        intent_display = {
            "order_status": "📦 Order Status",
            "delivery_status": "🚚 Delivery Status",
            "refund_status": "💰 Refund Status",
            "cancel_order": "❌ Cancel Order",
            "human_support": "👨‍💼 Human Support"
        }

        st.metric(
            "Intent",
            intent_display.get(
                result["intent"],
                result["intent"]
            )
        )

    with col2:

        st.metric(
            "Confidence",
            f"{result['confidence'] * 100:.0f}%"
        )

    with col3:

        st.metric(
            "Requires Human",
            "Yes" if result["requires_human"] else "No"
        )

    with col4:

        tool_map = {
            "order_status": "📦 Get Order Status",
            "delivery_status": "🚚 Get Delivery Status",
            "refund_status": "💰 Get Refund Status",
            "cancel_order": "❌ Cancel Order",
            "human_support": "👨‍💼 Create Support Ticket"
        }

        st.metric(
            "Tool Selected",
            tool_map.get(
                result["intent"],
                "-"
            )
        )

    st.divider()

    # --------------------------------
    # Final Agent Response
    # --------------------------------

    st.subheader("💬 Customer Response")

    st.write(
        result.get(
            "response",
            "I was unable to generate a response."
        )
    )
st.divider()

st.caption(
    "Version 1.0 | Python • Streamlit • PostgreSQL • Groq API • LLM Intent Classification • Tool Calling"
)
        

        