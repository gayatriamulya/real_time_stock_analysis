import requests
from bs4 import BeautifulSoup
import pandas as pd
import streamlit as st
import yfinance as yf
from textblob import TextBlob
import numpy as np
from langchain_mistralai import ChatMistralAI
from dotenv import load_dotenv
import os
import getpass

# os.environ["MISTRAL_API_KEY"] = getpass.getpass("Mistral API key: ")


# Load environment variables
load_dotenv()



# Function to fetch detailed stock data using yfinance
def fetch_stock_details(stock_symbol):
    stock = yf.Ticker(stock_symbol)
    
    # Get stock info (summary, sector, market cap, etc.)
    stock_info = stock.info
    
    # Get historical market data (for the last year)
    hist_data = stock.history(period="1y")
    
    # Get major holders
    major_holders = stock.major_holders
    
    # Get institutional holders
    institutional_holders = stock.institutional_holders
    
    # Get dividends
    dividends = stock.dividends

    # Get news
    news = stock.news
    
    # Compiling all data into a dictionary
    stock_details = {
        'info': stock_info,
        'history': hist_data,
        'major_holders': major_holders,
        'institutional_holders': institutional_holders,
        'dividends': dividends,
        'news': news
    }
    
    return stock_details

def analyze_data(stock_details):
    llm = ChatMistralAI(
        model="mistral-large-latest",  
        temperature=0.7,
        max_tokens=None,
        #timeout=None,
        #max_retries=2,
        api_key=os.getenv("MISTRAL_API_KEY")
        # base_url=" ",
        # organization=" ",
      
    )
    messages = [
        (
            "system",
            "You are a financial analyst. Tell whether to buy the stock or not based on the information given by user",
        ),
        (
            "human",
            f"Here is the stock information : {stock_details}."
        ),
    ]
    text = llm.invoke(messages)
    print(text.content)
    return text.content
