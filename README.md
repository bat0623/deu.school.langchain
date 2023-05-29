# 동의대학교 학사 정보 챗봇

## 개발환경

- [vscode](https://code.visualstudio.com/download)
- [python3.8](https://www.python.org/downloads/release/python-3810/)

## 설치

```bash
pip install -r requirements.txt
```

## 실행

```bash
echo "OPENAI_API_KEY=sk-" > .env
python main.py
streamlit run ./src/chat_ui.py
```

## 프롬프트 구성

```txt
{입력 문서}

이건 동의대학교 학사 시스템 인터페이스입니다.
모든 대답을 할 때, 수정일자가 있다면, 수정일자도 알려줘야 합니다.
```

## 가능한 질문
- 컴공 교수님 소개 페이지 알려줘
- 소프트웨어공학과 교수님 소개 페이지 알려줘
- 컴공에는 어떤 교수님이 있어?
- 강의평점이 4 이상인 강의를 알려주고 그 안에서 교수님 목록을 알려줘. 강의평점 상위 10명만
- 강의평점 상위 10위 안에 교수들의 교수님과 강의평점을 알려줘
- 강의평점 상위 10위 안에 교수들의 교수님과 강의명과 강의평점을 csv 형태로 알려줘
- 

## 참고 자료

- [프롬프트란?](https://tech.kakaoenterprise.com/188)