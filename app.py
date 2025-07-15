import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="findequity", layout="wide")
st.title("📈 findequity - Nifty 500 Stock Screener")

st.sidebar.header("🔍 Filters")

timeframe = st.sidebar.selectbox("Select Timeframe", ["2h", "1h", "4h", "daily", "monthly"])
indicator = st.sidebar.selectbox("Select Indicator", ["20 EMA", "30 SMA", "200 EMA"])
support_filter = st.sidebar.checkbox("Show Stocks Taking Support", value=True)

nifty_500 = pd.read_csv("nifty_500_list.csv")  # Stock list

def fetch_data(symbol):
    try:
        stock = yf.Ticker(symbol + ".NS")
        df = stock.history(period="90d", interval=timeframe)
        df["20ema"] = df["Close"].ewm(span=20, adjust=False).mean()
        df["30sma"] = df["Close"].rolling(window=30).mean()
        df["200ema"] = df["Close"].ewm(span=200, adjust=False).mean()
        return df
    except:
        return None

results = []

for symbol in nifty_500["Symbol"]:
    df = fetch_data(symbol)
    if df is None or df.empty:
        continue

    if indicator == "20 EMA":
        signal = df["Close"].iloc[-1] > df["20ema"].iloc[-1]
    elif indicator == "30 SMA":
        signal = df["Close"].iloc[-1] > df["30sma"].iloc[-1]
    elif indicator == "200 EMA":
        signal = df["Close"].iloc[-1] > df["200ema"].iloc[-1]

    if support_filter and signal:
        results.append(symbol)

st.subheader("📋 Stocks Matching Criteria:")
if results:
    st.write(results)
else:
    st.write("No stocks found.")
