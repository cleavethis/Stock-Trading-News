import requests
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

api_key = os.getenv("API_KEY")

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": api_key
}

time_now = datetime.now()
if time_now.weekday() == 0:
    # its monday, go get thurs/friday's data
    yesterday = str(time_now.date() - timedelta(days=3))
    day_before_yesterday = str(time_now.date() - timedelta(days=4))
elif time_now.weekday() == 1:
    # its tuesday, go get fri/mon data
    yesterday = str(time_now.date() - timedelta(days=1))
    day_before_yesterday = str(time_now.date() - timedelta(days=4))
else:
    yesterday = str(time_now.date() - timedelta(days=1))
    day_before_yesterday = str(time_now.date() - timedelta(days=2))




r = requests.get(STOCK_ENDPOINT, params=parameters)
data = r.json()


## STEP 1: Use https://newsapi.org/docs/endpoints/everything
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
#HINT 1: Get the closing price for yesterday and the day before yesterday. Find the positive difference between the two prices. e.g. 40 - 20 = -20, but the positive difference is 20.
#HINT 2: Work out the value of 5% of yerstday's closing stock price.
yesterday_close = float(data["Time Series (Daily)"][yesterday]["4. close"])
day_before_yesterday_close = float(data["Time Series (Daily)"][day_before_yesterday]["4. close"])

alert_threshold = .05 * yesterday_close
difference = abs(day_before_yesterday_close - yesterday_close)





## STEP 2: Use https://newsapi.org/docs/endpoints/everything
# Instead of printing ("Get News"), actually fetch the first 3 articles for the COMPANY_NAME. 
#HINT 1: Think about using the Python Slice Operator
if difference > alert_threshold:
    pass



## STEP 3: Use twilio.com/docs/sms/quickstart/python
# Send a separate message with each article's title and description to your phone number. 
#HINT 1: Consider using a List Comprehension.



#Optional: Format the SMS message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

