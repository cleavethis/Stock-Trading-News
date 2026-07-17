import requests
import os
from smtplib import SMTP
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

stock_api_key = os.getenv("STOCK_API_KEY")
news_api_key = os.getenv("NEWS_API_KEY")
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

def previous_business_day(date):
    offset = 3 if date.weekday() == 0 else 1
    return date - timedelta(days=offset)

stock_parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": stock_api_key
}

today = datetime.now().date()
yesterday = str(previous_business_day(today))
day_before_yesterday = str(previous_business_day(previous_business_day(today)))
                           
r = requests.get(STOCK_ENDPOINT, params=stock_parameters)
data = r.json()

## STEP 1: Use https://newsapi.org/docs/endpoints/everything
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
#HINT 1: Get the closing price for yesterday and the day before yesterday. Find the positive difference between the two prices. e.g. 40 - 20 = -20, but the positive difference is 20.
#HINT 2: Work out the value of 5% of yerstday's closing stock price.
yesterday_close = float(data["Time Series (Daily)"][yesterday]["4. close"])
day_before_yesterday_close = float(data["Time Series (Daily)"][day_before_yesterday]["4. close"])

alert_threshold = .05 * yesterday_close
difference = abs(day_before_yesterday_close - yesterday_close)
print(difference)




## STEP 2: Use https://newsapi.org/docs/endpoints/everything
# Instead of printing ("Get News"), actually fetch the first 3 articles for the COMPANY_NAME. 
#HINT 1: Think about using the Python Slice Operator
news_parameters = {
    "apiKey": news_api_key,
    "q": COMPANY_NAME,

}

if difference > alert_threshold:
    news = requests.get(NEWS_ENDPOINT, params=news_parameters)
    news_data = news.json()
    articles = news_data["articles"][:3]
    for a in articles:
        print(a["title"])
        print(a["description"])
        print()



## STEP 3: Use twilio.com/docs/sms/quickstart/python
# Send a separate message with each article's title and description to your phone number. 
#HINT 1: Consider using a List Comprehension.
