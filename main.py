import requests
import os
from smtplib import SMTP
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

stock_api_key = os.getenv("STOCK_API_KEY")
news_api_key = os.getenv("NEWS_API_KEY")
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
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

yesterday_close = float(data["Time Series (Daily)"][yesterday]["4. close"])
day_before_yesterday_close = float(data["Time Series (Daily)"][day_before_yesterday]["4. close"])

alert_threshold = .05 * yesterday_close
difference = abs(day_before_yesterday_close - yesterday_close)

news_parameters = {
    "apiKey": news_api_key,
    "q": COMPANY_NAME,

}

if difference >= alert_threshold:
    news = requests.get(NEWS_ENDPOINT, params=news_parameters)
    news_data = news.json()
    articles = news_data["articles"][:3]
    email_body = "\n\n".join(f"{a["title"]}\n{a["description"]}" for a in articles)

    with SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()
        connection.login(EMAIL,PASSWORD)
        connection.sendmail(from_addr=EMAIL, to_addrs=EMAIL, msg=f"Subject:TSLA 5% swing\n\n{email_body}".encode("utf-8"))