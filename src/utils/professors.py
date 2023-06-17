# -*- coding:utf-8 -*-
import os
import re
import csv
import requests
from tqdm import tqdm
from pprint import pprint
from datetime import datetime
from bs4 import BeautifulSoup

tel_pattern = re.compile(r"\d{2,3}[- ]?\d{3,4}[- ]?\d{4}")

current_path = os.path.dirname(os.path.realpath(__file__))
now = datetime.now()
with open(f"{current_path}/../../static/introduce.csv", "r") as f:
    rows = csv.DictReader(f)
    rows = list(rows)


def case_1_parse(rows, url):
    result = []
    for row in rows:
        교수이름 = row.find("h4").text.replace("교수", "").strip()
        obj = {"교수이름": 교수이름, "전화번호": None, "연구실": None, "전공": None, "이메일": None}
        for x in row.find_all("li"):
            title = str(x.find("span"))
            x = str(x.text.strip())
            if title.find("학위") != -1:
                obj["전공"] = x.replace("학위", "")
            if title.find("연구실") != -1:
                obj["연구실"] = x.replace("연구실", "")
            if title.find("전화번호") != -1:
                obj["전화번호"] = tel_pattern.findall(x)[0]
            if title.find("E-mail") != -1:
                obj["이메일"] = x.replace("E-mail", "")
        obj["출처"] = url
        obj["수정일자"] = str(now)
        result.append(obj)
    return result


def case_2_parse(rows, url):
    result = []
    for row in rows:
        obj = {
            "교수이름": row.find("p").text.strip(),
            "전화번호": None,
            "연구실": None,
            "전공": row.find("dt").find("span").text.strip(),
            "이메일": None,
        }
        for x in row.find_all("li"):
            title = str(x.find("span"))
            x = str(x.text.strip())
            if title.find("학위") != -1:
                obj["전공"] = x.replace("학위", "").strip()
            if title.find("연구실") != -1:
                obj["연구실"] = x.replace("연구실", "").strip()
            if title.find("연락처") != -1:
                if len(tel_pattern.findall(x)) > 0:
                    obj["전화번호"] = tel_pattern.findall(x)[0].strip()
                else:
                    obj["전화번호"] = x
            if title.find("E-MAIL") != -1:
                obj["이메일"] = x.replace("E-MAIL", "").strip()
        obj["출처"] = url
        obj["수정일자"] = str(now)
        result.append(obj)
    return result


result = []

for row in tqdm(rows):
    url = row["출처"]
    res = requests.get(url)
    res.encoding = "utf-8"  # 간혹, 인코딩이 꺠지는 페이지 대비하여 인코딩 고정
    soup = BeautifulSoup(res.text, "lxml")
    teachList = soup.find("div", {"class": "teachList"})
    if teachList == None:
        teachList = soup.find_all("div", {"class": "professor-item"})[:-1]
        if teachList != None and len(teachList) > 0:
            result.extend(case_1_parse(teachList, url))
    else:
        teachList = teachList.find_all("div", {"class": "box"})
        result.extend(case_2_parse(teachList, url))

with open(f"{current_path}/../../static/professors.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=result[0].keys())
    writer.writeheader()
    writer.writerows(result)
