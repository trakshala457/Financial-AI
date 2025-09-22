import os
from dotenv import load_dotenv
import google.generativeai as genai
import streamlit as st

from advisor import generate_financial_advice
from fraud_detector import get_transaction_embeddings, detect_anomalies
from tts_reporter import generate_audio_report

load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')
genai.configure(api_key=api_key)

st.set_page_config(page_title="AI Financial Advisor", layout="wide")
st.title("💰 AI Financial Advisor & Fraud Detection Platform")

with st.sidebar:
    st.header("Settings")
    run_button = st.button("Generate Report")
    st.markdown("---")
    st.info("Enter your details and click 'Generate Report' to get started.")

# --- Section 1: Financial Advice ---
st.header("Financial Goals & Transactions")
st.markdown("---")

financial_goals = st.text_area("What are your financial goals? (e.g., 'save for a down payment, retire early'), height=100)")
st.markdown("---")

st.subheader("Recent Transaction History")
st.markdown("Enetr a comma-sepearted list of transactions (e.g., 'rent: 1500, groceries: 400, coffee: 100').")
user_transactions = st.text_area("Your Transactions", height=150)

if run_button:
    if not financial_goals or not user_transactions:
        st.warning("Please enter your financial goals and transactions.")
    else:
        st.subheader("Generating Report...")

        with st.spinner("Analyzing goals and generating advice..."):
            advice = generate_financial_advice(financial_goals , user_transactions)
            st.success("Financila advice generated!")
            st.markdown(">>> Your Personalized Financial Report")
            st.write(advice)
            print(advice)

        with st.spinner("Detecting suspicious transactions..."):
            mock_transactions_list = [t.strip() for t in user_transactions.split(",")]
            transaction_embeddings = get_transaction_embeddings(mock_transactions_list)

            if transaction_embeddings is not None:
                anomalies = detect_anomalies(transaction_embeddings)

                st.markdown(">>> Fraud Detection Summary")
                if anomalies:
                    st.error("🚨 Suspicious Transactions Detected!")
                    for index in anomalies:
                        st.write(f"**Flagged:** {mock_transactions_list[index]}")
                    st.write("Recommendation: Please review these transactions and consider reporting them.")
                else:
                    st.success("✅ No suspicious activity detected today.")

        with st.spinner("Preparing your audio report..."):
            full_report_text = f"Daily Financial Health Report.\n\n{advice}\n\nFraud Detection Summary: "
            if anomalies:
                full_report_text += "Suspicious activity was detected. Please review your flagged transactions."
            else:
                full_report_text += "No suspicious activity was detected today."

            generate_audio_report(full_report_text)
            st.success("Audio report ready!")
            st.audio("daily_report.mp3", format="audio/mp3")