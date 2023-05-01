# -*- coding:utf-8 -*-
import requests
from datetime import datetime
from bs4 import BeautifulSoup


def 학과수집():
    now = datetime.now()
    res = requests.get("https://www.deu.ac.kr/www/content/185")
    soup = BeautifulSoup(res.content, "lxml")
    href_list = soup.select("a")
    for href in href_list:
        if "href" in href.attrs.keys():
            url = href["href"]
            if url != None and href.text.strip().endswith("과"):
                if url.endswith(".deu.ac.kr"):
                    row = (
                        "|["
                        + href.text
                        + "]"
                        + "("
                        + url
                        + "/"
                        + url.split("://")[1].split(".")[0]
                        + "/sub02.do)|"
                        + str(now)
                        + "|"
                    )
                    print(row)
                elif url.startswith("/www/dept/edu"):
                    row = (
                        "|["
                        + href.text
                        + "]"
                        + "(https://www.deu.ac.kr"
                        + url.replace("/edu", "/member").replace("/1", "/2")
                        + ")|"
                        + str(now)
                        + "|"
                    )
                    print(row)


학과수집()
