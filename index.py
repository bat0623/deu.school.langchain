# -*- coding:utf-8 -*-
import os
from pprint import pprint
from langchain.vectorstores import FAISS
from langchain.text_splitter import MarkdownTextSplitter

path = os.path.dirname(os.path.abspath(__file__))

with open(f"{path}/DEU_Menual.md", mode="r") as f:
    markdown_text = f.read()

markdown_splitter = MarkdownTextSplitter(chunk_size=100, chunk_overlap=0)

docs = markdown_splitter.create_documents([markdown_text])

for page in docs:
    pprint(page)
