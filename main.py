import requests
from twilio.rest import Client




STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_URL='https://www.alphavantage.co/query'
STOCK_API='API KEY FROM alphavantage.co'
NEWS_API='API KEY FROM newsapi.org'
NEWS_URL='https://newsapi.org/v2/everything'

para={
    'function':'TIME_SERIES_DAILY',
    'symbol':STOCK,
    'apikey':STOCK_API
}

#fetching date and curresponding close price of the stock
stock_data = requests.get(url=STOCK_API,params=para)
stock_data.raise_for_status()
daily_stock=stock_data.json()['Time Series (Daily)']
date=[]
close_price=[]
for keys in daily_stock:
    date.append(keys)
    close_price.append(float(daily_stock[keys]['4. close']))

#incrementing one day from date[0] for news api
news_dt=date[0].split('-')
list_1=[]
for dt in range(len(news_dt)):
    if dt==2:
        news_dt[dt]=f'0{int(news_dt[dt])+1}'
        list_1.append(news_dt[dt])
    else:
        list_1.append(news_dt[dt])
news_dt="-".join(list_1)

news_parameters={
    'apiKey':NEWS_API,
    'q':'tesla',
    'from':news_dt,
    'to':news_dt,
'sortBy':'popularity',
'language':'en',
}

#fetching the news
news= requests.get(url=NEWS_URL,params=news_parameters)
news.raise_for_status()
news_list=news.json()['articles']
news_date=[item['publishedAt'].split('T')[0] for item in news_list]
news_title=[item['title'] for item in news_list]
news_description=[item['description'] for item in news_list]

account_sid ='ACCOUNT SID FROM TWILIO'
auth_token ='AUTH TOKEN FROM TWILIO'


#Send each article as a separate message via Twilio.
client = Client(account_sid, auth_token)
avg=(abs((close_price[0]-close_price[1]))/close_price[0])*100
if close_price[0]>=close_price[1]:
    tit=f"Date:{date[0]}, TSLA: 🔺{round(avg,2)}%"
else:
    tit=f"Date:{date[0]}, TSLA: 🔻{round(avg,2)}%"
for n in range(3):
    if news_date[n]==news_dt:
        message = client.messages \
            .create(
            body=f"{tit}\n\nHeadline: {news_title[n]}\n\nBrief: {news_description[n]}\n",
            from_='+19036257355',
            to='RECIEVER MOBILE NUMBER'
        )
        print(message.status)
