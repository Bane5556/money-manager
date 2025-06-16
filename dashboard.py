import streamlit as st
import pandas as pd
from datetime import date
from db import connect_db
from models import Transaction, add_transaction

# Page config
st.set_page_config(page_title="💰 Money Manager", layout="wide")
st.title("💸 Money Manager Dashboard")

# 🔄 Load data with caching
@st.cache_data
def load_data():
    with connect_db() as conn:
        df = pd.read_sql_query("SELECT * FROM transactions", conn)
    return df

# 📥 Add New Transaction Form
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
        new_tx = Transaction(
            date=tx_date.strftime("%Y-%m-%d"),
            t_type=tx_type,
            category=tx_category,
            amount=tx_amount,
            person=tx_person,
            notes=tx_notes
        )
        add_transaction(new_tx)
        st.cache_data.clear()  # Clear cached data
        st.success("✅ Transaction added!")
        st.experimental_rerun()  # Rerun to refresh UI immediately

# 📊 Load and display transactions
df = load_data()

if df.empty:
    st.warning("No transactions found.")
else:
    st.dataframe(df)

    # 💼 Summary
    st.subheader("📈 Summary")
    total = df["amount"].sum()
    spend = df[df["type"] == "Spend"]["amount"].sum()
    borrow = df[df["type"] == "Borrow"]["amount"].sum()
    lend = df[df["type"] == "Lend"]["amount"].sum()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total", f"${total:.2f}")
    col2.metric("Spent", f"${spend:.2f}")
    col3.metric("Borrowed", f"${borrow:.2f}")
    col4.metric("Lent", f"${lend:.2f}")

    # 📊 Spending by Category (Bar Chart)
    st.subheader("🧾 Spending by Category")
    cat_group = df[df["type"] == "Spend"].groupby("category")["amount"].sum()
    if not cat_group.empty:
        st.bar_chart(cat_group)
    else:
        st.info("No spending data to show.")
