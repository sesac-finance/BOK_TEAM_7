#금리 데이터 크롤링
import requests
from bs4 import BeautifulSoup
import pandas as pd
from pandas import DataFrame

interest_rate_url = 'https://www.bok.or.kr/portal/singl/baseRate/list.do?dataSeCd=01&menuNo=200643'
rep = requests.get(interest_rate_url)
interest_rate_datas = BeautifulSoup(rep.text, 'html.parser')
interest_rate_datas = interest_rate_datas.find_all('tr')
interest_rate_date_list=[]
interest_rate_list=[]
for interest_rate_data in interest_rate_datas[1:]:
    interest_rate_date_list.append(interest_rate_data.text.split('\n')[1]+'년 '+interest_rate_data.text.split('\n')[2])
    interest_rate_list.append(interest_rate_data.text.split('\n')[3])

data = {
    '변경일자':interest_rate_date_list,
    '기준금리':interest_rate_list
}

df= DataFrame(data)
df.to_csv('interest_rate_result.csv')