
import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="Sales Dashboard", layout="wide")

st.title("📊 Monthly Sales Dashboard")

uploaded_file = st.file_uploader("Upload your CSV file", type="csv")
month = st.text_input("Enter Month (e.g. July)", "")
goal = st.number_input("Enter Sales Goal (£)", value=0)

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    df['SALES'] = pd.to_numeric(df['SALES'], errors='coerce').fillna(0)

    selected_rep = st.selectbox("Filter by Salesperson", options=["All"] + sorted(df['SALES PERSON'].unique().tolist()))

    if selected_rep != "All":
        df = df[df['SALES PERSON'] == selected_rep]

    total_sales = df['SALES'].sum()
    st.markdown(f"### 💰 Total Sales for {month or 'Selected Month'}: £{int(total_sales):,}")

    # Chart
    chart_data = df.groupby('SALES PERSON')['SALES'].sum().reset_index()
    chart_data['GOAL'] = goal

    chart = alt.Chart(chart_data).transform_fold(
        ['SALES', 'GOAL'],
        as_=['Metric', 'Value']
    ).mark_bar().encode(
        x='SALES PERSON:N',
        y='Value:Q',
        color='Metric:N',
        column='Metric:N'
    ).properties(width=150, height=400)

    st.altair_chart(chart, use_container_width=True)

    # Download
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("Download Filtered Data", data=csv, file_name="filtered_sales_report.csv", mime="text/csv")
else:
    st.info("Please upload a CSV file to get started.")
