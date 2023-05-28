# -*- coding:utf-8 -*-
import csv
import requests
from bs4 import BeautifulSoup

url = "https://www.deu.ac.kr/www/content/57"

filename = "convenience_place.csv"
f = open(filename, "w", encoding="utf-8-sig", newline="")
writer = csv.writer(f)

# 페이지 요청
res = requests.get(url)

# BeautifulSoup으로 HTML 파싱
soup = BeautifulSoup(res.text, "html.parser")

# 시설별 위치 정보 테이블 찾기
table = soup.find("table", attrs={"class": "table table-line text-center"})

# 제목 행 가져오기
title_row = None
for row in table.find_all("tr"):
    if row.find("th"):
        title_row = row
        break

titles = [title.get_text() for title in title_row.find_all("th")]

# 시설별 위치 정보 가져오기
data_rows = table.find_all("tr")[1:]  # 첫 번째 행은 제목 행이므로 제외하고 가져옵니다.

writer.writerow(["건물명", "층수", "편의시설", "출처"])
for row in data_rows:
    data_cells = row.find_all("td")
    size = len(data_cells)

    if size == 3:
        facility = data_cells[0].get_text().strip()
    location = data_cells[size - 2].get_text()
    description = data_cells[size - 1].get_text()
    writer.writerow([facility, location, description, url])

f.close()
