# -*- coding:utf-8 -*-
import os
import re
import sys
import time
import itertools
from glob import glob
from typing import List
from langchain import OpenAI
from dotenv import load_dotenv
from fastapi import Body, FastAPI
from langchain import PromptTemplate
from langchain.schema import Document
from langchain.vectorstores import FAISS
from langchain.agents import create_csv_agent
from langchain.document_loaders import CSVLoader
from langchain.embeddings.openai import OpenAIEmbeddings


path = os.path.dirname(os.path.abspath(__file__))
SCR_PATH = os.path.abspath(__file__)
SCR_DIR, SCR_BN = os.path.split(SCR_PATH)
REPO_DIR = os.path.abspath(SCR_DIR + "/..")
ASSETS_DIR = os.path.abspath(REPO_DIR + "/static")
csv_list = glob(ASSETS_DIR + "/*.csv")

templates = {
    "case1": """ChatGPT 모델을 다음 지침을 따르세요.
1. 대답을 할 때는 부드러운 말투로 대답해야 합니다.
2. 대답을 할 때는 안내하듯이 대답해야 합니다.
3. 대답을 할 때는 반드시 출처를 반드시 알려줘야 합니다.
---
'{input_text}'라는 질문에 대한 대답은 '{output_text}'입니다.""",
    "case2": """ChatGPT 모델을 다음 지침을 따르세요.
1. 대답을 할 때는 부드러운 말투로 대답해야 합니다.
2. 대답을 할 때는 안내하듯이 대답해야 합니다.
3. 반드시 한국어로 대답해야합니다.
4. 당신은 동의대학교에 대한 정보만 대답해야 합니다.
5. '하지만'과 같은 대답을 해서는 안됩니다.
6. 모든 대답에서는 출처를 남겨줘야합니다.
7. 출처를 반드시 알려줘야 합니다.
---
'{input_text}'라는 질문에 대한 대답은 '{output_text}'입니다.""",
}


try:
    load_dotenv()
    apikey = os.environ["OPENAI_API_KEY"]
except:
    print("Please, export your OpenAI API KEY over 'OPENAI_API_KEY' environment variable")
    print("You may create the key here: https://platform.openai.com/account/api-keys")
    sys.exit(1)


app = FastAPI()


def csv_parser(query, filePath):
    llm = OpenAI(temperature=0, model_name="text-davinci-003")
    agent = create_csv_agent(llm, filePath, verbose=True, kwargs={"max_iterations": 5})
    res = agent.run(query)
    return res


def load_files(query) -> List[Document]:
    embeddings = OpenAIEmbeddings()
    docs = [
        CSVLoader(file, csv_args={"delimiter": ",", "quotechar": '"'}).load()
        for file in filter(lambda x: x.endswith("menual.csv"), csv_list)
    ]
    docs = list(itertools.chain(*docs))
    db = FAISS.from_documents(docs, embeddings)
    retriever = db.as_retriever(search_kwargs={"k": 1})
    docs = retriever.get_relevant_documents(query)
    return docs


@app.post("/chat")
async def submit_chat(
    query: str = Body(..., embed=True),
):
    res = load_files(query)
    if len(res) > 0:
        pattern = r"filename: (\S+\.csv)"
        match = re.search(pattern, res[0].page_content.split("\n")[0])
        fileName = match.group(1)
        res = csv_parser(query=query, filePath=(ASSETS_DIR + "/" + fileName))
        prompt = PromptTemplate(
            input_variables=["input_text", "output_text"],
            template=templates["case1"],
        )
        print(res)
        texts = prompt.format_prompt(input_text=query, output_text=res)
        model = OpenAI(model_name="text-davinci-003", temperature=0.0)
        result = model(texts.to_string())
        return {"state": "OK", "output_text": result + "\n출처는 다음과 같습니다.\n" + res}
    else:
        return {
            "state": "ERROR",
            "output_text": "현재 저에게는 관련된 자료를 찾을 수 없습니다.😭\n해당 내용은 업데이트 할 수 있도록 하겠습니다.",
        }
