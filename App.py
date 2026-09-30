import streamlit as st
import pandas as pd
import plotly.express as px

# Page settings
st.set_page_config(
    page_title="Sales Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Sales Analytics Dashboard")

# Load data
uploaded_file = st.file_uploader("Upload Sales CSV File", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # Convert date
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"])

    st.subheader("Dataset")
    st.dataframe(df, use_container_width=True)

    # KPIs
    total_sales = df["Sales"].sum()
    total_profit = df["Profit"].sum()
    total_orders = df["Order ID"].nunique()

    col1, col2, col3 = st.columns(3)

    col1.metric("💰 Total Sales", f"₹{total_sales:,.0f}")
    col2.metric("📈 Total Profit", f"₹{total_profit:,.0f}")
    col3.metric("🛒 Total Orders", total_orders)

    st.divider()

    # Sales by category
    if "Category" in df.columns:
        category_sales = (
            df.groupby("Category")["Sales"]
            .sum()
            .reset_index()
        )

        fig1 = px.bar(
            category_sales,
            x="Category",
            y="Sales",
            title="Sales by Category"
        )

        st.plotly_chart(fig1, use_container_width=True)

    # Sales by region
    if "Region" in df.columns:
        region_sales = (
            df.groupby("Region")["Sales"]
            .sum()
            .reset_index()
        )

        fig2 = px.pie(
            region_sales,
            names="Region",
            values="Sales",
            title="Sales by Region"
        )

        st.plotly_chart(fig2, use_container_width=True)

    # Monthly sales
    if "Date" in df.columns:
        monthly_sales = (
            df.groupby(df["Date"].dt.to_period("M"))["Sales"]
            .sum()
            .reset_index()
        )

        monthly_sales["Date"] = monthly_sales["Date"].astype(str)

        fig3 = px.line(
            monthly_sales,
            x="Date",
            y="Sales",
            markers=True,
            title="Monthly Sales Trend"
        )

        st.plotly_chart(fig3, use_container_width=True)

    # Top products
    if "Product" in df.columns:
        top_products = (
            df.groupby("Product")["Sales"]
            .sum()
            .sort_values(ascending=False)
            .head(10)
            .reset_index()
        )

        fig4 = px.bar(
            top_products,
            x="Sales",
            y="Product",
            orientation="h",
            title="Top 10 Products"
        )

        st.plotly_chart(fig4, use_container_width=True)

else:
    st.info("Please upload your sales CSV file.")
