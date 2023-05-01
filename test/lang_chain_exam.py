# -*- coding:utf-8 -*-
import os
import sys
import pickle
from langchain import OpenAI
from dotenv import load_dotenv
from langchain import PromptTemplate
from langchain.chains import LLMChain
from langchain.vectorstores import FAISS
from langchain.text_splitter import MarkdownTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.document_loaders import UnstructuredMarkdownLoader
from langchain.chains import ConversationalRetrievalChain
from langchain.chains.qa_with_sources import load_qa_with_sources_chain

path = os.path.dirname(os.path.abspath(__file__))
SCR_PATH = os.path.abspath(__file__)
SCR_DIR, SCR_BN = os.path.split(SCR_PATH)
REPO_DIR = os.path.abspath(SCR_DIR + "/..")
CHAT_HISTORY = REPO_DIR + "/." + SCR_BN + "-chat-history.pk"

try:
    load_dotenv()
    apikey = os.environ["OPENAI_API_KEY"]
except:
    print("Please, export your OpenAI API KEY over 'OPENAI_API_KEY' environment variable")
    print("You may create the key here: https://platform.openai.com/account/api-keys")
    sys.exit(1)


loader = UnstructuredMarkdownLoader(f"{path}/../DEU_Menual.md", mode="elements")
docs = loader.load()

text_splitter = MarkdownTextSplitter(chunk_size=1000, chunk_overlap=50)
texts = text_splitter.split_documents(docs)

embeddings = OpenAIEmbeddings()
vectorstore = FAISS.from_documents(texts, embeddings)
retriever = vectorstore.as_retriever()

llm = OpenAI(temperature=0)


template = """
This is the interface of Dong-eui University's academic system.
When answering all the questions, you need to give the revision date, if any, and answer in Korean.
Given the following conversation and a follow up question, rephrase the follow up question to be a standalone question.

Chat History:
{chat_history}
Follow Up Input: {question}
Standalone question:"""

question_generator = LLMChain(llm=llm, prompt=PromptTemplate.from_template(template))
doc_chain = load_qa_with_sources_chain(llm, chain_type="map_reduce")

qa = ConversationalRetrievalChain(
    retriever=retriever,
    question_generator=question_generator,
    combine_docs_chain=doc_chain,
)
chat_history = []

try:
    with open(CHAT_HISTORY, "rb") as f:  # open in binary mode
        chat_history = pickle.load(f)  # Deserialize the array from the file
except:
    pass

while True:
    query = input("\n무엇이든 무엇보세요 (0 = quit): ")
    if query == "0":
        break
    result = qa({"question": query, "chat_history": chat_history})
    answer = result["answer"]
    print(answer)
    chat_history.append((query, answer))

print("\n[채팅 기록 저장...]\n")
with open(CHAT_HISTORY, "wb") as f:  # write in binary mode
    pickle.dump(chat_history, f)  # serialize the array and write it to the file

print("종료 !")
