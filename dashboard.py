import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# Load data
@st.cache_data
def load_data():
    df = pd.read_json('data.json')
    # Preprocess data
    df['invoice_date'] = pd.to_datetime(df['invoice_date'], format='%m/%d/%y')
    df['age'] = df['age'].astype(int)
    df['quantity'] = df['quantity'].astype(int)
    df['total_price'] = df['total_price'].astype(float)
    return df

df = load_data()

# Title
st.title("Shopping Mall Sales Dashboard")
st.markdown("Analyze sales data from shopping malls with interactive filters and KPIs.")

# Sidebar filters
st.sidebar.header("Filters")

# Date range filter
min_date = df['invoice_date'].min().date()
max_date = df['invoice_date'].max().date()
date_range = st.sidebar.date_input(
    "Select Date Range",
    [min_date, max_date],
    min_value=min_date,
    max_value=max_date
)

# Category filter
categories = st.sidebar.multiselect(
    "Select Categories",
    options=df['category'].unique(),
    default=df['category'].unique()
)

# Shopping mall filter
malls = st.sidebar.multiselect(
    "Select Shopping Malls",
    options=df['shopping_mall'].unique(),
    default=df['shopping_mall'].unique()
)

# Gender filter
genders = st.sidebar.multiselect(
    "Select Gender",
    options=df['gender'].unique(),
    default=df['gender'].unique()
)

# Payment method filter
payments = st.sidebar.multiselect(
    "Select Payment Methods",
    options=df['payment_method'].unique(),
    default=df['payment_method'].unique()
)

# Age group filter
age_bins = [0, 18, 25, 35, 45, 55, 65, 100]
age_labels = ['<18', '18-24', '25-34', '35-44', '45-54', '55-64', '65+']
df['age_group'] = pd.cut(df['age'], bins=age_bins, labels=age_labels, right=False)
age_groups = st.sidebar.multiselect(
    "Select Age Groups",
    options=df['age_group'].unique(),
    default=df['age_group'].unique()
)

# Filter data
filtered_df = df[
    (df['invoice_date'].dt.date >= date_range[0]) &
    (df['invoice_date'].dt.date <= date_range[1]) &
    (df['category'].isin(categories)) &
    (df['shopping_mall'].isin(malls)) &
    (df['gender'].isin(genders)) &
    (df['payment_method'].isin(payments)) &
    (df['age_group'].isin(age_groups))
]

# KPIs
total_sales = filtered_df['total_price'].sum()
total_transactions = len(filtered_df)
avg_order_value = total_sales / total_transactions if total_transactions > 0 else 0
unique_customers = filtered_df['customer_id'].nunique()
total_quantity = filtered_df['quantity'].sum()

# Display KPIs
st.header("Key Performance Indicators")
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Total Sales", f"${total_sales:,.2f}")
col2.metric("Total Transactions", f"{total_transactions:,}")
col3.metric("Average Order Value", f"${avg_order_value:,.2f}")
col4.metric("Unique Customers", f"{unique_customers:,}")
col5.metric("Total Items Sold", f"{total_quantity:,}")

# Charts
st.header("Sales Analysis")

# Sales by Category
st.subheader("Sales by Category")
category_sales = filtered_df.groupby('category')['total_price'].sum().reset_index().sort_values('total_price', ascending=False)
fig1 = px.bar(category_sales, x='category', y='total_price', title="Total Sales by Category",
              labels={'total_price': 'Sales ($)', 'category': 'Category'})
st.plotly_chart(fig1, use_container_width=True)

# Sales by Shopping Mall
st.subheader("Sales by Shopping Mall")
mall_sales = filtered_df.groupby('shopping_mall')['total_price'].sum().reset_index().sort_values('total_price', ascending=False)
fig2 = px.bar(mall_sales, x='shopping_mall', y='total_price', title="Total Sales by Shopping Mall",
              labels={'total_price': 'Sales ($)', 'shopping_mall': 'Shopping Mall'})
st.plotly_chart(fig2, use_container_width=True)

# Monthly Sales Trend
st.subheader("Monthly Sales Trend")
monthly_sales = filtered_df.groupby(filtered_df['invoice_date'].dt.to_period('M'), observed=False)['total_price'].sum().reset_index()
monthly_sales['invoice_date'] = monthly_sales['invoice_date'].astype(str)
fig3 = px.line(monthly_sales, x='invoice_date', y='total_price', title="Monthly Sales Over Time",
               labels={'total_price': 'Sales ($)', 'invoice_date': 'Month'})
st.plotly_chart(fig3, use_container_width=True)

# Payment Method Distribution
st.subheader("Payment Method Distribution")
payment_dist = filtered_df['payment_method'].value_counts().reset_index()
payment_dist.columns = ['payment_method', 'count']
fig4 = px.pie(payment_dist, names='payment_method', values='count', title="Distribution of Payment Methods")
st.plotly_chart(fig4, use_container_width=True)

# Gender Distribution
st.subheader("Sales by Gender")
gender_sales = filtered_df.groupby('gender')['total_price'].sum().reset_index()
fig5 = px.bar(gender_sales, x='gender', y='total_price', title="Total Sales by Gender",
              labels={'total_price': 'Sales ($)', 'gender': 'Gender'})
st.plotly_chart(fig5, use_container_width=True)

# Age Group Analysis
st.subheader("Sales by Age Group")
age_sales = filtered_df.groupby('age_group')['total_price'].sum().reset_index()
fig6 = px.bar(age_sales, x='age_group', y='total_price', title="Total Sales by Age Group",
              labels={'total_price': 'Sales ($)', 'age_group': 'Age Group'})
st.plotly_chart(fig6, use_container_width=True)

# Data Table
st.header("Filtered Data")
st.dataframe(filtered_df.head(100))  # Show first 100 rows for performance

# Footer
st.markdown("---")
st.markdown("Dashboard created with Streamlit. Data analysis powered by Pandas and Plotly.")