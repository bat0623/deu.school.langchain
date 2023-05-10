import requests
import pandas as pd
from bs4 import BeautifulSoup

i=1
Data=[]

while(1):
    url = 'https://www.deu.ac.kr/www/board/3/'
    url = url+str(i)
    i+=1
    response = requests.get(url)

    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')

        for k in range(1,11):
            num =soup.select_one("#tablelist > tbody > tr:nth-child(%s) > th"%str(k))
            title=soup.select_one("#tablelist > tbody > tr:nth-child(%s) > td.text-left"%str(k))
            href=soup.select_one("#tablelist > tbody > tr:nth-child(%s) > td.text-left > a:nth-child(1)"%str(k))
            link="https://www.deu.ac.kr"+href.attrs['href']
            day=soup.select_one("#tablelist > tbody > tr:nth-child(%s) > td:nth-child(4)"%str(k))
            
            Data.append(num.get_text()+","+title.get_text()+","+link+","+day.get_text())

            if (num.get_text()!="1"):
                print(num.get_text()+","+title.get_text()+","+link+","+day.get_text())
            else:
                print(num.get_text()+","+title.get_text()+","+link+","+day.get_text())
                break


    else :
        print(response.status_code)

    if(num.get_text()=="1"):
        break


df = pd.DataFrame(Data)
df.columns=['번호,공지사항,링크,작성일']
df.to_csv('공지사항.csv', index=False)

