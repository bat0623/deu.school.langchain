# -*- coding:utf-8 -*-
import requests
from datetime import datetime
from bs4 import BeautifulSoup


def 학과수집():
    now = datetime.now()  # 현재 시간 가져오기
    target_url = "https://www.deu.ac.kr/www/content/185"  # 크롤링할 타겟 사이트 url
    res = requests.get(target_url)  # 타겟 사이트 url에 http get 요청
    soup = BeautifulSoup(res.content, "lxml")  # 타겟 사이트로부터 응답한 HTML 파일 파싱
    # lxml을 사용하는 이유는 표준을 지킨 html 파일은 거의 없기 때문에 유연하게 대응하기 위해 xml과 html 둘다 파싱이 가능하도록 해주기 때문에 사용함
    a_tag_list = soup.select("a")  # 파싱한 html 파일에서 a 태그를 가진 모든 요소를 배열로 가져온다.
    for a_tag in a_tag_list:  # 배열을 순회한다.
        if "href" in a_tag.attrs.keys():  # a 태그의 속성은 dict 구조로 되어 있는데, 속성 안에 href 속성이 있는지 확인한다.
            url = a_tag["href"]  # a 태그 안에서 href 속성 값(url 경로)을 꺼낸다.
            if url != None and a_tag.text.strip().endswith("과"):
                """
                # 안정적인 코드 진행을 위해 None 체크 후 a 태그 안에 있는 텍스트 요소를 꺼내고
                # 앞뒤로 의미 없는 문자를 제거 후 해당 문자열의 마지막이 '과'로 끝나는 a 태그만 체크합니다.
                """
                # html 분석 결과 별도의 서브 도메인이 있는 학과와 홈페이지 내부 경로로 이어지는 경우가 있습니다.
                if url.endswith(".deu.ac.kr"):  # 별도의 서브 도메인이 있는 경우
                    row = (
                        "|["
                        + a_tag.text
                        + "]"
                        + "("
                        + url
                        + "/"
                        + url.split("://")[1].split(".")[0]
                        + "/sub02.do)|"
                        + str(now)
                        + "|"
                    )
                    # 마크다운에서 table 구조로 데이터를 만들기 위한 목적
                    print(row)
                elif url.startswith("/www/dept/edu"):  # 홈페이지 내부 경로로 이어지는 경우
                    row = (
                        "|["
                        + a_tag.text
                        + "]"
                        + "(https://www.deu.ac.kr"
                        + url.replace("/edu", "/member").replace("/1", "/2")
                        + ")|"
                        + str(now)
                        + "|"
                    )
                    # 마크다운에서 table 구조로 데이터를 만들기 위한 목적
                    print(row)


if __name__ == "__main__":
    학과수집()
