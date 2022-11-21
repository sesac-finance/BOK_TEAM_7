# 채권 사이트 크롤링
import openpyxl
import requests
from bs4 import BeautifulSoup
# start_num 은 크롤링 시작 코드값
# end_num 은 크롤링 마지막 코드값
def crawling_bond_xlex(start_num, end_num):
    wb = openpyxl.Workbook()
    sheet = wb.active
    sheet['A1']='날짜'
    sheet['B1']='채권분석pdf링크'
    for num in range(start_num, end_num):
        try:
            # url 불러오기      
            url = 'https://finance.naver.com/research/economy_read.naver?nid={num}&page=1'.format(num=num)
            response = requests.get(url)
            print(num)
            # url 내용을 bond_site(채권_사이트) 로 정의
            bond_site = BeautifulSoup(response.text, 'html.parser')
            # date_info == 해당 보고서 업로드 날짜 정보

            # url 사이트에 pdf 파일 링크 가져오기
            bond_pdf_link = bond_site.find('th', class_='view_report')
            bond_pdf_link=bond_pdf_link.select('a')
            bond_pdf_link=bond_pdf_link[0].attrs['href']
            # bond_pdf_link 는 해당 pdf 파일의 링크
            print(bond_pdf_link)
            
            # date_info 는 해당 pdf 파일의 업로드 날짜
            date_info = bond_site.find('p', class_='source')
            date_info = date_info.text.split('|')[1]
            print(date_info)
            # 엑셀 시트에 추가해주기
            sheet.append([date_info, bond_pdf_link])
            
        except:
            pass
    # 엑셀 파일 저장
    wb.save('bond_list.xlsx')

# 채권 사이트 크롤링 한 곳에 내부 텍스트 내용 추가
import pandas as pd
import pdftotext
df = pd.read_excel('bond_list.xlsx',engine='openpyxl')
contexts=[]
files = pd.read_excel('bond_list.xlsx',usecols=[1])
files_values=files.values
print(files_values)
print(files.values[0][0].split('/')[-1])
for file_value in files_values:
    file = open('pdf_info/{file_num}'.format(file_num=file_value[0].split('/')[-1]),'rb')
    try:
        fileReader = pdftotext.PDF(file)

        pages = ''
        for page in fileReader:
            pages += page.replace('\n', '')
    except:
        pass
    contexts.append(pages)
    print(len(contexts))

df['내용'] = contexts
df.head()
df.to_csv('bond_list_result.csv')