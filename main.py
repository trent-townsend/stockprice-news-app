import requests
from datetime import date, datetime, timedelta
import pytz
import os
from twilio.rest import Client

STOCK = "TSLA"
COMPANY_NAME = "Tesla"

ALPHA_API_KEY = os.environ['ALPHA_API_KEY']
NEWS_API = os.environ['NEWS_API']
SMS_ACCOUNT_SID = os.environ['SMS_ACCOUNT_SID']
SMS_AUTH_TOKEN = os.environ['SMS_AUTH_TOKEN']
TO_PHONE_NUM = os.environ['TO_PHONE_NUM']
FROM_PHONE_NUM = os.environ['FROM_PHONE_NUM']

# Determine date in US/EST time currently
us_est = pytz.timezone("US/Eastern")
now_est = (datetime.now(us_est)).date() - timedelta(days=1)
yesterday_us_est = now_est - timedelta(days=1)


def send_sms():
    #fetch news
    news_parameters = {
        "q": COMPANY_NAME,
        "country": "us",
        "category": "business",
        "int": "3",
        "apiKey": NEWS_API
    }

    news_requests = requests.get(
        url="https://newsapi.org/v2/top-headlines", params=news_parameters)
    news_requests.raise_for_status()
    news_data = news_requests.json()["articles"]
    news_info = [{'title': article['title'], 'description': article['description'],
                'url':article['url']} for article in news_data]

    # Compose SMS message
    n = 0
    msg = f"{STOCK}: {direction}{perc_delta_price}%"
    for article in news_info:
        msg = msg + \
            f"\nHeadline: {news_info[n]['title']}\nDescription: {news_info[n]['description']}\nRead More: {news_info[n]['url']}"
        n += 1

    # Send text message containing news articles

    client = Client(SMS_ACCOUNT_SID, SMS_AUTH_TOKEN)
    message = client.messages \
        .create(
            body=msg,
            from_=FROM_PHONE_NUM,
            to=TO_PHONE_NUM
        )


# Get request for stock data
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

# Determine % change in stock price between today's open and yesterday's close
most_recent_open = float(data_today['1. open'])
yesterday_close = float(data_yesterday['4. close'])
perc_delta_price = round(
    (abs(most_recent_open - yesterday_close) / yesterday_close) * 100, 2)

if most_recent_open > yesterday_close:
    direction = '🔺'
else:
    direction = '🔻'

# Fetch news articles relating to company if % change >=5%
if perc_delta_price >= 5:
    send_sms()
else:
    pass 