# app.py
import streamlit as st
import plotly.graph_objects as go
from stock_data import get_stock_data
from analyst import get_latest_news, analyse_stock
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(Path(__file__).parent / ".env")
# Page setup
st.set_page_config(
    page_title="Stock AI Analyst",
    page_icon="📈",
    layout="wide"
    # layout wide = full screen width
)

st.title("📈 Stock AI Analyst")
st.write("Enter a stock symbol to get AI powered analysis")

# Input section
col1, col2 = st.columns([3, 1])
# creates 2 columns, first is 3x wider
# col1 = input box, col2 = button

with col1:
    symbol = st.text_input(
        "Enter Stock Symbol",
        placeholder="e.g. TCS.NS, RELIANCE.NS, INFY.NS"
    )

with col2:
    analyse_btn = st.button(
        "Analyse",
        use_container_width=True
    )

# Common Indian stocks guide
st.info("""
💡 Indian Stock Symbols:
TCS → TCS.NS | Reliance → RELIANCE.NS | 
Infosys → INFY.NS | HDFC Bank → HDFCBANK.NS
""")

# When button is clicked
if analyse_btn and symbol:

    # Step 1 - Fetch stock data
    with st.spinner(f"Fetching data for {symbol}..."):
        stock_data = get_stock_data(symbol)

    if "error" in stock_data:
        st.error(f"Error: {stock_data['error']}")
        # show error if symbol is wrong
    else:
        # Step 2 - Show key metrics in columns
        st.subheader(f"📊 {stock_data['company_name']}")

        m1, m2, m3, m4 = st.columns(4)
        # 4 equal columns for metrics

        m1.metric(
            "Current Price",
            f"₹{stock_data['current_price']}"
        )
        m2.metric(
            "30D Change",
            f"{stock_data['change_30d_percent']}%"
        )
        m3.metric(
            "52W High",
            f"₹{stock_data['52_week_high']}"
        )
        m4.metric(
            "PE Ratio",
            stock_data['pe_ratio']
        )
        # st.metric shows a nice card with label and value

        # Step 3 - Price chart
        st.subheader("📉 Price Chart (Last 30 Days)")

        history = stock_data['history']

        fig = go.Figure()
        # go.Figure creates a plotly chart

        fig.add_trace(go.Scatter(
            x=history.index,
            # x axis = dates
            y=history['Close'],
            # y axis = closing prices
            mode='lines',
            name='Close Price',
            line=dict(color='#00ff88', width=2)
        ))

        fig.update_layout(
            xaxis_title="Date",
            yaxis_title="Price (₹)",
            template="plotly_dark",
            height=400
        )

        st.plotly_chart(fig, use_container_width=True)
        # shows chart full width

        # Step 4 - Fetch news
        with st.spinner("Fetching latest news..."):
            news = get_latest_news(
                stock_data['company_name']
            )

        # Step 5 - AI Analysis
        with st.spinner("Generating AI analysis..."):
            report = analyse_stock(stock_data, news)

        # Step 6 - Show report
        st.subheader("🤖 AI Analyst Report")
        st.markdown(report)
        # st.markdown renders formatted text nicely

        # Step 7 - Show raw news in expander
        with st.expander("📰 View Raw News Sources"):
            st.write(news)