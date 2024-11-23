import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go


# data
# df = pd.read_csv('../01_data/data.csv', delimiter=';')
# df = pd.read_csv('./01_data/data.csv', delimiter=';')

df = pd.read_csv('01_data/data.csv', delimiter=';')
df['DATE'] = pd.to_datetime(df['DATE'], format='%m/%d/%Y')
df['DAU'] = df['DAU'].replace({',': ''}, regex=True).astype(float)
df['Inapp Revenue'] = df['Inapp Revenue'].replace({',': '', r'\$': '', ' ': ''}, regex=True).astype(float)
df['Ad Revenue'] = df['Ad Revenue'].replace({'\\$': '', ',': '', ' ': '', '-': '0'}, regex=True).astype(float)
df['Total Revenue'] = df['Inapp Revenue'] + df['Ad Revenue']
df['Revenue per DAU'] = df['Total Revenue'] / df['DAU']


# 14-day rolling averages
df['14-day avg DAU'] = df['DAU'].rolling(window=14, min_periods=1).mean()
df['14-day avg Total Revenue'] = df['Total Revenue'].rolling(window=14, min_periods=1).mean()


# player segmentation
median_inapp_revenue = df['Inapp Revenue'].median()
df['Player Segment'] = df.apply(
    lambda row: 'Non-Payer' if row['Inapp Revenue'] == 0 
    else 'Mid-Payer' if row['Inapp Revenue'] <= median_inapp_revenue 
    else 'Heavy-Payer', axis=1
)


# summary metrics
df_segment_summary = df.groupby(['Player Segment'])[['DAU', 'Total Revenue']].sum().reset_index()
df_revenue_sources = df[['Ad Revenue', 'Inapp Revenue', 'Total Revenue']].sum().reset_index(name='Revenue')


# dashboard
st.title("AB Testing for Gamers | KPI Dashboard")


# KPIs section with descriptions
st.header("Key Performance Indicators")
st.write("""
This section presents the most important KPIs, including DAU, Total Revenue, ARPU, and Ad Revenue Share.
- **DAU (Daily Active Users)**: Total number of unique users engaging with the game daily.
- **Total Revenue**: The sum of revenue generated from both In-App Purchases and Ad Revenue.
- **ARPU (Average Revenue Per User)**: Shows the average revenue generated per user.
- **Ad Revenue Share**: The percentage of total revenue that comes from Ad Revenue.
""")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total DAU", f"{df['DAU'].sum():,.0f}")
col2.metric("Total Revenue", f"${df['Total Revenue'].sum():,.2f}")
col3.metric("ARPU", f"${df['Total Revenue'].sum() / df['DAU'].sum():.2f}")
col4.metric("Ad Revenue Share", f"{(df['Ad Revenue'].sum() / df['Total Revenue'].sum()) * 100:.2f}%")


# DAU and revenue trends
st.header("DAU and Revenue Trends")
st.write("""
This section displays trends in DAU and Total Revenue over time, helping to visualize the game's growth.
- The chart shows how DAU and Total Revenue have evolved over time, allowing us to spot growth or decline.
""")
revenue_trend = go.Figure()
revenue_trend.add_trace(go.Scatter(x=df['DATE'], y=df['DAU'], mode='lines', name='DAU', line=dict(color='blue')))
revenue_trend.add_trace(go.Scatter(x=df['DATE'], y=df['Total Revenue'], mode='lines', name='Total Revenue', line=dict(color='green')))
revenue_trend.update_layout(title="DAU & Total Revenue Over Time", xaxis_title="Date", yaxis_title="Value")
st.plotly_chart(revenue_trend)


# player segmentation funnel
st.header("Player Segmentation Funnel")
st.write("""
This chart illustrates how DAU is distributed among different player segments (Non-Payers, Mid-Payers, and Heavy-Payers).
- It helps to understand how users are distributed across different revenue-generating categories.
""")
segmentation_fig = px.bar(df_segment_summary, x="Player Segment", y="DAU", title="DAU by Player Segment")
segmentation_fig.update_layout(xaxis_title="Player Segment", yaxis_title="DAU")
st.plotly_chart(segmentation_fig)


# revenue distribution
st.header("Revenue Distribution")
st.write("""
This pie chart shows the breakdown of total revenue by source (Ad Revenue, In-App Purchases).
- It helps to understand where the majority of revenue is coming from and informs monetization strategy.
""")
revenue_dist_fig = px.pie(df_revenue_sources, names='index', values='Revenue', title="Revenue Distribution by Source")
st.plotly_chart(revenue_dist_fig)


# ad revenue vs. in-app revenue
st.header("Ad Revenue vs. In-App Revenue")
st.write("""
This chart compares the Ad Revenue and In-App Revenue over time, showing how both revenue streams contribute to the overall revenue.
- This is useful for assessing the effectiveness of different monetization strategies.
""")
revenue_sources_trend = go.Figure()
revenue_sources_trend.add_trace(go.Scatter(x=df['DATE'], y=df['Ad Revenue'], mode='lines', name='Ad Revenue', line=dict(color='orange')))
revenue_sources_trend.add_trace(go.Scatter(x=df['DATE'], y=df['Inapp Revenue'], mode='lines', name='In-App Revenue', line=dict(color='purple')))
revenue_sources_trend.update_layout(title="Ad Revenue vs. In-App Revenue", xaxis_title="Date", yaxis_title="Revenue")
st.plotly_chart(revenue_sources_trend)


# 14-day rolling averages
st.header("14-Day Rolling Averages")
st.write("""
This chart shows 14-day rolling averages of DAU and Total Revenue. It smooths out short-term fluctuations and gives a better view of longer-term trends.
- Useful for understanding sustained performance and trends over a two-week period.
""")
rolling_fig = go.Figure()
rolling_fig.add_trace(go.Scatter(x=df['DATE'], y=df['14-day avg DAU'], mode='lines', name='14-day avg DAU', line=dict(color='blue')))
rolling_fig.add_trace(go.Scatter(x=df['DATE'], y=df['14-day avg Total Revenue'], mode='lines', name='14-day avg Revenue', line=dict(color='green')))
rolling_fig.update_layout(title="14-day Rolling Averages of DAU & Total Revenue", xaxis_title="Date", yaxis_title="Value")
st.plotly_chart(rolling_fig)


# raw data table
# st.subheader("Raw Data")
# st.write(df)

st.write("""
### Recommended Additional KPIs and Metrics:
- **Retention Rate (Day 1, Day 7, Day 30)**: Measures how many players come back after 1, 7, and 30 days, indicating player loyalty.
- **Conversion Rate**: The percentage of Non-Payers who become Mid or Heavy Payers, showing the effectiveness of monetization strategies.
- **Test vs. Control Revenue Growth**: Helps evaluate the impact of new features like "rewarded ads" by comparing revenue from test and control groups.
- **Lifetime Value (LTV)**: Estimates total revenue per player over their entire lifecycle.
- **Churn Rate**: Measures the percentage of users lost over a period, providing early insights into potential engagement issues.
""")