from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.docstore.document import Document
from dotenv import load_dotenv
import openai
import os
import re
import requests

# получим переменные окружения из .env
load_dotenv()

# API-key
openai.api_key = os.environ.get("OPENAI_API_KEY")

# задаем system
default_system = "Ты-консультант в компании Simble, ответь на вопрос клиента на основе документа с информацией. Не придумывай ничего от себя, отвечай максимально по документу. Не упоминай Документ с информацией для ответа клиенту. Клиент ничего не должен знать про Документ с информацией для ответа клиенту"

data_url = 'https://docs.google.com/document/d/11MU3SnVbwL_rM-5fIC14Lc3XnbAV4rY1Zd_kpcMuH4Y'
default_system_url = 'https://docs.google.com/document/d/1mwdXqx50imzvtPPbp7l8BTf3JsrUYQ0g2NhAwsjssJ8/edit?usp=sharing'
class Chunk():

    def load_document_text(self, url: str) -> str:
        # Extract the document ID from the URL
        match_ = re.search('/document/d/([a-zA-Z0-9-_]+)', url)
        if match_ is None:
            raise ValueError('Invalid Google Docs URL')
        doc_id = match_.group(1)

        # Download the document as plain text
        response = requests.get(f'https://docs.google.com/document/d/{doc_id}/export?format=txt')
        response.raise_for_status()
        text = response.text

        return text

    def __init__(self, path_to_base: str, sep: str = " ", ch_size: int = 1024, ch_overlap: int = 128):

        # загружаем базу
        # with open(path_to_base, 'r', encoding='utf-8') as file:
        #     document = file.read()
        data_from_url = self.load_document_text(path_to_base)
        # создаем список чанков
        source_chunks = []
        # splitter = CharacterTextSplitter(separator=sep, chunk_size=ch_size)
        # for chunk in splitter.split_text(document):
        #     source_chunks.append(Document(page_content=chunk, metadata={}))

        splitter = RecursiveCharacterTextSplitter(chunk_size=ch_size, chunk_overlap=ch_overlap,
                                                  length_function=len)  # заполните нужными значениями, проведите эксперименты
        for chunk in splitter.split_text(data_from_url):
            source_chunks.append(Document(page_content=chunk, metadata={}))

        # создаем индексную базу
        embeddings = OpenAIEmbeddings()
        self.db = FAISS.from_documents(source_chunks, embeddings)

    def get_answer(self, system_url: str = default_system_url, query: str = None):
        '''Функция получения ответа от chatgpt
        '''
        system = self.load_document_text(system_url)
        # релевантные отрезки из базы
        docs = self.db.similarity_search(query, k=4)
        message_content = '\n'.join([f'{doc.page_content}' for doc in docs])
        messages = [
            {"role": "system", "content": system},
            {"role": "user",
             "content": f"Ответь на вопрос клиента. Не упоминай документ с информацией для ответа клиенту в ответе. Документ с информацией для ответа клиенту: {message_content}\n\nВопрос клиента: \n{query}"}
        ]

        # получение ответа от chatgpt
        completion = openai.ChatCompletion.create(model="gpt-4o-mini",
                                                  messages=messages,
                                                  temperature=0)

        return completion.choices[0].message.content

