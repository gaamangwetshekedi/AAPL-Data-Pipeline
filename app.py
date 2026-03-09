import streamlit as st
import pandas as pd
import os

# Configuration of streamlit and Fabric
st.set_page_config(page_title="AAPL Dashboard", layout="wide")

DAILY_PATH = r"C:\Users\gaamangwet1\Downloads\daily aapl.csv"
WEEKLY_PATH = r"C:\Users\gaamangwet1\Downloads\weekly aapl.csv"

# Data Loading
@st.cache_data(ttl=3600)
def load_data():
    daily_df = pd.read_csv(DAILY_PATH)
    weekly_df = pd.read_csv(WEEKLY_PATH)
    
    daily_df["Date"] = pd.to_datetime(daily_df["Date"])
    weekly_df["Week"] = pd.to_datetime(weekly_df["week"])
    
    daily_df = daily_df.sort_values("Date")
    weekly_df = weekly_df.sort_values("Week")
    
    return daily_df, weekly_df

daily_df, weekly_df = load_data()

# Metrics
latest = daily_df.iloc[-1]
prev = daily_df.iloc[-2]

st.title("📈 AAPL Dashboard")
st.caption(f"Last updated: {latest['Date'].strftime('%Y-%m-%d')}")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Close Price", f"${latest['close']:.2f}", f"{latest['pct_change']:+.2f}%")
col2.metric("Open", f"${latest['open']:.2f}")
col3.metric("MA 7", f"${latest['ma_7']:.2f}")
col4.metric("MA 30", f"${latest['ma_30']:.2f}")

st.divider()

# ----------------------------
# DAILY PRICE CHART
# ----------------------------
st.subheader("Daily Price & Moving Averages")

import plotly.graph_objects as go

fig_daily = go.Figure()
fig_daily.add_trace(go.Scatter(x=daily_df["date"], y=daily_df["close"], name="Close", line=dict(color="#1f77b4")))
fig_daily.add_trace(go.Scatter(x=daily_df["date"], y=daily_df["ma_7"], name="MA 7", line=dict(color="orange", dash="dash")))
fig_daily.add_trace(go.Scatter(x=daily_df["date"], y=daily_df["ma_30"], name="MA 30", line=dict(color="red", dash="dash")))
fig_daily.update_layout(xaxis_title="Date", yaxis_title="Price (USD)", hovermode="x unified")
st.plotly_chart(fig_daily, use_container_width=True)

st.divider()

# ----------------------------
# % CHANGE OVER TIME
# ----------------------------
st.subheader("Daily % Change")

fig_pct = go.Figure()
fig_pct.add_trace(go.Bar(
    x=daily_df["date"],
    y=daily_df["pct_change"],
    marker_color=daily_df["pct_change"].apply(lambda x: "green" if x >= 0 else "red")
))
fig_pct.update_layout(xaxis_title="Date", yaxis_title="% Change", hovermode="x unified")
st.plotly_chart(fig_pct, use_container_width=True)

st.divider()

# ----------------------------
# WEEKLY CHART
# ----------------------------
st.subheader("Weekly OHLCV")

fig_weekly = go.Figure(data=[go.Candlestick(
    x=weekly_df["week"],
    open=weekly_df["open"],
    high=weekly_df["high"],
    low=weekly_df["low"],
    close=weekly_df["close"]
)])
fig_weekly.update_layout(xaxis_title="Week", yaxis_title="Price (USD)")
st.plotly_chart(fig_weekly, use_container_width=True)
