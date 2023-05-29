import requests
import pandas as pd
from bs4 import BeautifulSoup

i = 1
num_data = []
title_data = []
link_data = []
day_data = []

while 1:
    url = "https://www.deu.ac.kr/www/board/3/"
    url = url + str(i)
    i += 1
    response = requests.get(url)

    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, "lxml")

        for k in range(1, 11):
            num = soup.select_one("#tablelist > tbody > tr:nth-child(%s) > th" % str(k))
            title = soup.select_one("#tablelist > tbody > tr:nth-child(%s) > td.text-left" % str(k))
            href = soup.select_one(
                "#tablelist > tbody > tr:nth-child(%s) > td.text-left > a:nth-child(1)" % str(k)
            )
            link = "https://www.deu.ac.kr" + href.attrs["href"]
            day = soup.select_one(
                "#tablelist > tbody > tr:nth-child(%s) > td:nth-child(4)" % str(k)
            )

            num_data.append(num.get_text())
            title_data.append(title.get_text())
            link_data.append(link)
            day_data.append(day.get_text())

            if num.get_text() != "1":
                print(num.get_text() + "," + title.get_text() + "," + link + "," + day.get_text())
            else:
                print(num.get_text() + "," + title.get_text() + "," + link + "," + day.get_text())
                break

    else:
        print(response.status_code)

    if num.get_text() == "1":
        break

Data = {"순번": num_data, "공지사항": title_data, "출처": link_data, "작성일": day_data}
df = pd.DataFrame(Data)

df.to_csv("notice.csv", index=False)
