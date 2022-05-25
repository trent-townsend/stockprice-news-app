from urllib import request
import requests 
from datetime import date, datetime, timedelta 
import os

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

yesterday = str(date.today() - timedelta(days=1))
two_days_ago = str(date.today() - timedelta(days=2))

#Get request for stock data 
ALPHA_API_KEY = os.environ['ALPHA_API_KEY']


api_parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol" : "TSLA",
    "outputsize" : "compact",
    "apikey" : ALPHA_API_KEY
}

alpha_requests = requests.get(url="https://www.alphavantage.co/query", params=api_parameters)
alpha_requests.raise_for_status()
data = alpha_requests.json()

#Extract two days most recent data
data_yesterday = data["Time Series (Daily)"][yesterday]
data_two_days_ago = data["Time Series (Daily)"][two_days_ago]
