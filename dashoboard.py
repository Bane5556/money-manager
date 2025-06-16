import streamlit as st
import pandas as pd
from db import connect_db
from datetime import date
from main import Transaction, add_transaction



st.set_page_config(page_title="💰 Money Manager", layout="wide")
st.title("💸 Money Manager Dashboard")

@st.cache_data
def load_data():
    with connect_db() as conn:
        df = pd.read_sql_query("SELECT * FROM transactions", conn)
    return df


df = load_data()

if df.empty:
    st.warning("No transactions found.")
else:
    st.dataframe(df)

    # Summary
    st.subheader("💼 Summary")
    total = df["amount"].sum()
    spend = df[df["type"] == "Spend"]["amount"].sum()
    borrow = df[df["type"] == "Borrow"]["amount"].sum()
    lend = df[df["type"] == "Lend"]["amount"].sum()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total", f"${total:.2f}")
    col2.metric("Spent", f"${spend:.2f}")
    col3.metric("Borrowed", f"${borrow:.2f}")
    col4.metric("Lent", f"${lend:.2f}")

    # Pie chart
    st.subheader("📊 Spending by Category")
    cat_group = df[df["type"] == "Spend"].groupby("category")["amount"].sum()
    st.bar_chart(cat_group)
st.header("➕ Add New Transaction")

with st.form("add_transaction_form"):
    tx_date = st.date_input("Date", value=date.today())
    tx_type = st.selectbox("Type", ["Spend", "Borrow", "Lend"])
    tx_category = st.text_input("Category", placeholder="e.g. Food, Rent")
    tx_amount = st.number_input("Amount", min_value=0.0, format="%.2f")
    tx_person = st.text_input("Person (optional)")
    tx_notes = st.text_area("Notes (optional)")

    submitted = st.form_submit_button("Add Transaction")

    if submitted:
        # Create a transaction object
        new_tx = Transaction(
            date=tx_date.strftime("%Y-%m-%d"),
            t_type=tx_type,
            category=tx_category,
            amount=tx_amount,
            person=tx_person,
            notes=tx_notes
        )
        add_transaction(new_tx)
        st.success("✅ Transaction added!")

