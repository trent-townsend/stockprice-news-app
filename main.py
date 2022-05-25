
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

api_parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": "TSLA",
    "outputsize": "compact",
    "apikey": ALPHA_API_KEY
}

alpha_requests = requests.get(
    url="https://www.alphavantage.co/query", params=api_parameters)
alpha_requests.raise_for_status()
data = alpha_requests.json()


# Extract two days most recent data

data_today = data["Time Series (Daily)"][str(now_est)]
data_yesterday = data["Time Series (Daily)"][str(yesterday_us_est)]

print(data_today)
print(data_yesterday)