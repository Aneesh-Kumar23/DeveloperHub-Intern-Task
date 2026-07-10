import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------------
# Page Configuration
# -------------------------
st.set_page_config(
    page_title="Global Superstore Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Global Superstore Interactive Dashboard")

# -------------------------
# Load Dataset
# -------------------------
df = pd.read_csv("Global_Superstore2.csv", encoding="latin1")

# -------------------------
# Data Cleaning
# -------------------------
df.drop_duplicates(inplace=True)

df["Order Date"] = pd.to_datetime(df["Order Date"])

# -------------------------
# Sidebar Filters
# -------------------------
st.sidebar.header("Filters")

region = st.sidebar.multiselect(
    "Select Region",
    options=sorted(df["Region"].unique()),
    default=sorted(df["Region"].unique())
)

category = st.sidebar.multiselect(
    "Select Category",
    options=sorted(df["Category"].unique()),
    default=sorted(df["Category"].unique())
)

sub_category = st.sidebar.multiselect(
    "Select Sub-Category",
    options=sorted(df["Sub-Category"].unique()),
    default=sorted(df["Sub-Category"].unique())
)

# -------------------------
# Filter Data
# -------------------------
filtered_df = df[
    (df["Region"].isin(region)) &
    (df["Category"].isin(category)) &
    (df["Sub-Category"].isin(sub_category))
]

# -------------------------
# KPI Cards
# -------------------------
total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()

col1, col2 = st.columns(2)

col1.metric("Total Sales", f"${total_sales:,.2f}")
col2.metric("Total Profit", f"${total_profit:,.2f}")

# -------------------------
# Sales by Category
# -------------------------
st.subheader("Sales by Category")

sales_category = (
    filtered_df.groupby("Category")["Sales"]
    .sum()
    .reset_index()
)

fig = px.bar(
    sales_category,
    x="Category",
    y="Sales",
    color="Category",
    text_auto=True
)

st.plotly_chart(fig, use_container_width=True)

# -------------------------
# Profit by Region
# -------------------------
st.subheader("Profit by Region")

profit_region = (
    filtered_df.groupby("Region")["Profit"]
    .sum()
    .reset_index()
)

fig = px.bar(
    profit_region,
    x="Region",
    y="Profit",
    color="Region",
    text_auto=True
)

st.plotly_chart(fig, use_container_width=True)

# -------------------------
# Top 5 Customers
# -------------------------
st.subheader("Top 5 Customers by Sales")

top_customers = (
    filtered_df.groupby("Customer Name")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(5)
    .reset_index()
)

fig = px.bar(
    top_customers,
    x="Customer Name",
    y="Sales",
    color="Sales",
    text_auto=True
)

st.plotly_chart(fig, use_container_width=True)

# -------------------------
# Sales by Segment
# -------------------------
st.subheader("Sales by Segment")

segment_sales = (
    filtered_df.groupby("Segment")["Sales"]
    .sum()
    .reset_index()
)

fig = px.pie(
    segment_sales,
    names="Segment",
    values="Sales",
    hole=0.4
)

st.plotly_chart(fig, use_container_width=True)

# -------------------------
# Monthly Sales Trend
# -------------------------
st.subheader("Monthly Sales Trend")

monthly_sales = (
    filtered_df.groupby(
        filtered_df["Order Date"].dt.to_period("M")
    )["Sales"]
    .sum()
    .reset_index()
)

monthly_sales["Order Date"] = monthly_sales["Order Date"].astype(str)

fig = px.line(
    monthly_sales,
    x="Order Date",
    y="Sales",
    markers=True
)

st.plotly_chart(fig, use_container_width=True)

# -------------------------
# Filtered Dataset
# -------------------------
st.subheader("Filtered Dataset")

st.dataframe(filtered_df)

# -------------------------
# Download Button
# -------------------------
csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    "⬇ Download Filtered Dataset",
    csv,
    "Filtered_Global_Superstore.csv",
    "text/csv"
)