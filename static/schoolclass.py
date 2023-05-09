import re
import numpy as np

f = open('C:/Users/TWCOM/Desktop/original.txt', 'r', encoding = 'UTF-8') #HTML 파일을 그대로 붙여넣은 원본 텍스트 파일
text = f.read()
text = re.sub('<td class="small"></td>', '<td class="small">-</td>', text)
text = re.sub('<td></td>', '<td>-</td>', text)
text = re.sub(', ', '|', text)
text = re.sub('<tbody>|</tbody>|<tr>|</tr>|<td>|<td class="bold">|<a href="/lecture/view/\d*" target="_blank" title="|" class="star"><span class="on" style="width: [\d|.]*%;"></span></a>|<td class="small">', '', text)
text = re.sub('</td>', '$', text) #텍스트 파일에서 정규식으로 데이터 추출

tary = text.split('$')
tary.pop()
npt = np.array(tary)
print(npt)
npt = npt.reshape(-1, 13) #추출한 데이터를 형식에 맞게 넘파이 배열로 함
f.close()

np.savetxt('C:/Users/TWCOM/Desktop/edited.csv', npt, fmt = '%s', delimiter = ',', newline = '\n', header = '과목코드, 과목명, 교수, 강의시간, 강의실, 구분, 학년, 학점, 강의평점, 담은 인원, 정원, 수강대상, 비고') #csv파일로 저장
#이후 수기로 일부 수정을 거침
