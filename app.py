import streamlit as st
from scraper import fetch_stock_details, analyze_data


# Streamlit UI
st.title("Real-Time Stock Analysis and Prediction")

# Input for stock ticker
ticker = st.text_input("Enter stock ticker symbol:", value="AAPL")

# Initialize session state variables
if 'stock_details' not in st.session_state:
    st.session_state.stock_details = None
if 'stock_prices' not in st.session_state:
    st.session_state.stock_prices = {}

# Fetch and display stock details
if st.button("Get Stock Details"):
    st.session_state.stock_details = fetch_stock_details(ticker)
    st.session_state.stock_prices[ticker] = st.session_state.stock_details['history']['Close'].iloc[-1]
    
    # Display basic stock info
    st.write(f"Company: {st.session_state.stock_details['info'].get('shortName', 'N/A')}")
    st.write(f"Sector: {st.session_state.stock_details['info'].get('sector', 'N/A')}")
    st.write(f"Market Cap: {st.session_state.stock_details['info'].get('marketCap', 'N/A')}")
    st.write(f"Current Stock Price: ${st.session_state.stock_prices[ticker]:.2f}")
    
    # Display dividends and splits
    st.write("Dividends:")
    st.write(st.session_state.stock_details['dividends'].tail())
    st.write("News:")
    st.write(st.session_state.stock_details['news'])

# Analyze data using sentiment analysis and indicators
if st.button("Analyze Data"):
    if st.session_state.stock_details is not None:
        result = analyze_data(st.session_state.stock_details)
        st.write(result)  
    else:
        st.write("Please fetch stock prices and news first.")
