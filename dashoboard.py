import streamlit as st
import pandas as pd
from db import connect_db

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
