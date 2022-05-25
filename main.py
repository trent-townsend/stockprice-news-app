import requests
from datetime import date, datetime, timedelta
import pytz
import os

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

# Determine date in US/EST time currently
us_est = pytz.timezone("US/Eastern")
now_est = (datetime.now(us_est)).date() - timedelta(days=1)
yesterday_us_est = now_est - timedelta(days=1)

# #Get request for stock data
ALPHA_API_KEY = os.environ['ALPHA_API_KEY']

stock_parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": "TSLA",
    "outputsize": "compact",
    "apikey": ALPHA_API_KEY
}

alpha_requests = requests.get(
    url="https://www.alphavantage.co/query", params=stock_parameters)
alpha_requests.raise_for_status()
data = alpha_requests.json()

# Extract two days most recent data
data_today = data["Time Series (Daily)"][str(now_est)]
data_yesterday = data["Time Series (Daily)"][str(yesterday_us_est)]

#Determine % change in stock price between today's open and yesterday's close 
most_recent_open = float(data_today['1. open'])
yesterday_close = float(data_yesterday['4. close'])
perc_delta_price = (abs(most_recent_open - yesterday_close) / yesterday_close) * 100


#Fetch news articles relating to company if % change >=5%
# if perc_delta_price >= 5:
    NEWS_API = os.environ['NEWS_API']

    news_parameters = {
        "q": COMPANY_NAME,
        "country": "us",
        "category": "business",
        "int": "3",
        "apiKey": NEWS_API
    }

    news_requests = requests.get(url="https://newsapi.org/v2/top-headlines", params=news_parameters)
    news_requests.raise_for_status()
    news_data = news_requests.json()
