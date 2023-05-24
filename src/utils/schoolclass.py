import re
import numpy as np
import os

path = os.path.dirname(os.path.abspath(__file__))
SCR_PATH = os.path.abspath(__file__)
SCR_DIR, SCR_BN = os.path.split(SCR_PATH)
REPO_DIR = os.path.abspath(SCR_DIR + "/..")
ASSETS_DIR = os.path.abspath(REPO_DIR + "/static")
html_path = os.path.join(ASSETS_DIR, "every_time_lecture_list_for_deu.html")
# 레포지토리에서 HTML 파일 가져오기

with open(html_path, "r", encoding="utf-8") as f:
    text = f.read()

text = re.sub(', ', '|', text)
text = re.sub('\s', '', text)
text = re.sub('<tdclass="small"></td>', '<tdclass="small">-</td>', text)
text = re.sub('<td></td>', '<td>-</td>', text)
text = re.sub('<table>\w*</thead>|<tbody>|</tbody>|<tr>|</tr>|<td>|<tdclass="bold">|<ahref="/lecture/view/\d*"target="_blank"title="|"class="star"><spanclass="on"style="width:[\d|.]*%;"></span></a>|<tdclass="small">', '', text)
text = re.sub('</td>', '$', text) #텍스트 파일에서 정규식으로 데이터 추출

tary = text.split('$')
tary.pop()
npt = np.array(tary)
npt = npt.reshape(-1, 13) #추출한 데이터를 형식에 맞게 넘파이 배열로 함
f.close()

np.savetxt('classSchedule.csv', npt, fmt = '%s', delimiter = ',', newline = '\n', header = '과목코드, 과목명, 교수, 강의시간, 강의실, 구분, 학년, 학점, 강의평점, 담은 인원, 정원, 수강대상, 비고') #csv파일로 저장
#이후 수기로 일부 수정을 거침
