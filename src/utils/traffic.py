import requests
import pandas as pd
from bs4 import BeautifulSoup

url = "https://www.deu.ac.kr/www/content/13"

bus_data = []
course_data = []
ref_url_list = []
response = requests.get(url)

if response.status_code == 200:
    html = response.text
    soup = BeautifulSoup(html, "lxml")
    for i in range(1, 4):
        bus = soup.select_one(
            "#content > div > div:nth-child(3) > table > tbody > tr:nth-child(%s) > td:nth-child(1)"
            % str(i)
        )
        bus_data.append(bus.get_text())

    time = soup.select_one(
        "#content > div > div:nth-child(3) > table > tbody > tr:nth-child(1) > td:nth-child(2)"
    )
    interval = soup.select_one(
        "#content > div > div:nth-child(3) > table > tbody > tr:nth-child(1) > td:nth-child(3)"
    )
    course6 = soup.select_one(
        "#content > div > div:nth-child(3) > table > tbody > tr:nth-child(1) > td:nth-child(4)"
    )
    course6_1 = soup.select_one(
        "#content > div > div:nth-child(3) > table > tbody > tr:nth-child(3) > td:nth-child(2)"
    )
    course9 = soup.select_one(
        "#content > div > div:nth-child(3) > table > tbody > tr:nth-child(2) > td:nth-child(2)"
    )
    course_data.append(course6.get_text())
    course_data.append(course6_1.get_text())
    course_data.append(course9.get_text())
    ref_url_list.append(url)


else:
    print(response.status_code)

Data = {
    "버스번호": bus_data,
    "배차시작시간": time.get_text().split(" ~ ")[0],
    "배차종료시간": time.get_text().split(" ~ ")[1],
    "간격": interval.get_text(),
    "경로": course_data,
    "출처": ref_url_list,
}
df = pd.DataFrame(Data)

df.to_csv("traffic.csv", index=False)
