import streamlit as st
import datetime
from fetcher import fetch_stock_data
from predictor import train_model, predict_price
import pandas as pd

st.set_page_config(page_title="🌍 Global Stock Predictor", layout="wide")

st.title("📈 Global Stock Price Predictor")

st.markdown("Enter two stock tickers to compare and predict their future prices.")

col1, col2 = st.columns(2)
ticker1 = col1.text_input("Enter First Stock Ticker:", value="AAPL")
ticker2 = col2.text_input("Enter Second Stock Ticker:", value="TSLA")

end_date = datetime.date.today()
start_date = end_date - datetime.timedelta(days=180)

if st.button("🔍 Compare & Predict"):
    data1 = fetch_stock_data(ticker1, start_date, end_date)
    data2 = fetch_stock_data(ticker2, start_date, end_date)

    if data1 is None or data2 is None:
        st.error("Couldn't fetch one or both stock data. Check ticker symbols.")
    else:
        st.success("Fetched data successfully.")

        st.subheader("📊 Historical Price Comparison")
        chart_data = pd.DataFrame({ticker1: data1['Close'], ticker2: data2['Close']})
        st.line_chart(chart_data)

        model1 = train_model(data1)
        model2 = train_model(data2)

        current_price1 = data1['Close'][-1]
        current_price2 = data2['Close'][-1]

        predicted_price1 = predict_price(model1, current_price1)
        predicted_price2 = predict_price(model2, current_price2)

        st.markdown(f"### {ticker1} → 📉 Current: `{current_price1:.2f}` | 🔮 5-day Forecast: `{predicted_price1:.2f}`")
        st.markdown(f"### {ticker2} → 📉 Current: `{current_price2:.2f}` | 🔮 5-day Forecast: `{predicted_price2:.2f}`")

        if st.checkbox("📥 Export Data to Excel"):
            export_df = pd.concat([data1['Close'], data2['Close']], axis=1)
            export_df.columns = [ticker1, ticker2]
            export_df.to_excel("stock_comparison.xlsx")
            st.success("Exported as stock_comparison.xlsx ✅")

st.markdown("---")
st.markdown("🌗 **Toggle Theme in Streamlit Settings (Top-Right Menu)**")
