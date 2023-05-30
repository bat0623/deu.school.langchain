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
    "case1": """'{input_text}'라는 질문에 대한 대답은 '{output_text}'입니다. 이를 안내하듯이 부드러운 말투로 대답해주세요. 대답할 때는 줄임말을 쓰지 않아야 합니다. """
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
    # agent = create_csv_agent(llm, filePath, verbose=True, kwargs={"max_iterations": 5})
    agent = create_csv_agent(llm, filePath, verbose=False, kwargs={"max_iterations": 5})
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
        pattern = r"파일명: (\S+\.csv)"
        match = re.search(pattern, res[0].page_content.split("\n")[0])
        fileName = match.group(1)
        res = csv_parser(query=query, filePath=(ASSETS_DIR + "/" + fileName))
        prompt = PromptTemplate(
            input_variables=["input_text", "output_text"],
            template=templates["case1"],
        )
        texts = prompt.format_prompt(input_text=query, output_text=res)
        model = OpenAI(model_name="text-davinci-003", temperature=0.0)
        result = model(texts.to_string())
        return {"state": "OK", "output_text": result}
    else:
        return {
            "state": "ERROR",
            "output_text": "현재 저에게는 관련된 자료를 찾을 수 없습니다.😭\n해당 내용은 업데이트 할 수 있도록 하겠습니다.",
        }
