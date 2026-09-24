import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Predictive CLV Engine", layout="wide")
st.title("📊 Predictive Customer Lifetime Value (CLV) Segmentation Engine")
st.markdown("---")

st.sidebar.header("🎓 Evaluation Details")
st.sidebar.info("**Course:** Innovation & Entrepreneurship\n\n**Code:** 01BMBAR24363")

st.header("📂 1. Upload Transactional Data")
uploaded_file = st.file_uploader("Upload business transaction logs (CSV)", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    df['Purchase_Date'] = pd.to_datetime(df['Purchase_Date'])
    
    total_customers = df['Customer_ID'].nunique()
    avg_order_value = df['Order_Value'].mean()
    purchase_frequency = len(df) / total_customers
    predicted_clv_val = avg_order_value * purchase_frequency * 3.0
    
    st.header("📈 2. Core Business Diagnostics")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total User Base", f"{total_customers} Users")
    c2.metric("Avg Basket Value", f"₹{avg_order_value:,.2f}")
    c3.metric("Purchase Frequency", f"{purchase_frequency:.2f} times/yr")
    c4.metric("Avg Projected CLV", f"₹{predicted_clv_val:,.2f}")
    
    customer_metrics = df.groupby('Customer_ID').agg(Total_Revenue=('Order_Value', 'sum'), Purchase_Count=('Order_Value', 'count')).reset_index()
    def categorize(row):
        return "High-Value Loyalists" if row['Total_Revenue'] > customer_metrics['Total_Revenue'].median() else "Low-Value Occasional Buyers"
    
    customer_metrics['Cohort_Segment'] = customer_metrics.apply(categorize, axis=1)
    
    st.header("🎯 3. Predictive Segment Cohorts")
    fig = px.pie(customer_metrics, names='Cohort_Segment', values='Total_Revenue', title="Revenue Distribution by Cohort")
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("👋 Please upload your transactional CSV file to view the analysis live.")
