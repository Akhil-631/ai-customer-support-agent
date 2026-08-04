import streamlit as st

from agent import (
    classify_intent,
    route_intent
)

st.set_page_config(
    page_title="Enterprise AI Customer Support Agent",
    page_icon="🤖",
    layout="wide"
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

            result = classify_intent(user_query)

            response = route_intent(
                result,
                user_query
            )

        st.divider()

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
                f"{result['confidence']*100:.0f}%"
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

        if result["intent"] == "order_status":

            lines = response.split("\n")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("📦 Order Status", lines[0].replace("Order Status: ", ""))

            with col2:
                st.metric("🚚 Delivery", lines[1].replace("Delivery Status: ", ""))

            with col3:
                st.metric("📅 Expected", lines[2].replace("Expected Delivery: ", ""))


        else:
            if result["intent"] == "human_support":
                st.warning(response)

            elif result["intent"] == "cancel_order":
                st.success(response)

            elif result["intent"] == "refund_status":
                st.info(response)

            else:
                st.success(response)

st.divider()

st.caption(
    "Version 1.0 | Python • Streamlit • PostgreSQL • Groq API • LLM Intent Classification • Tool Calling"
)
        

        