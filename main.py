from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from chunks import Chunk
from pydantic import BaseModel
#from langchain_core.pydantic_v1 import BaseModel
from dotenv import load_dotenv
import os

# uvicorn main:app --port 5000

# подгружаем переменные окружения
load_dotenv()

# передаем секретные данные в переменные
TOKEN = os.environ.get("TG_TOKEN")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

# инициализация индексной базы
data_url = 'data.txt'
chunk = Chunk(path_to_base=data_url)


# класс с типами данных параметров
class Item(BaseModel):
    text: str


# создаем объект приложения
app = FastAPI()
# настройки для работы запросов
app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# функция обработки get запроса + декоратор
@app.get("/")
def read_root():
    return {"message": "answer"}

# функция, которая обрабатывает запрос по пути "/count"
@app.get("/count")
def count():
    return {"message": chunk.count}

# функция обработки post запроса + декоратор
@app.post("/api/get_answer")
def get_answer(question: Item):
    answer = chunk.get_answer(query=question.text)
    return {"message": answer}
