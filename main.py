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
    history: str


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

# асинхронная функция обработки post запроса + декоратор
@app.post("/api/get_answer_async")
async def get_answer_async(question: Item):
    print(f"question.text - {question.text}\nquestion.history - {question.history}")
    history = question.history if question.history else None
    answer = await chunk.async_get_answer(query=question.text, history=question.history)
    return {"message": answer}

# асинхронная функция обработки post запроса + декоратор
@app.post("/api/summarize_question_async")
async def summarize_question_async(question: Item):
    print(f"question.text - {question.text}\nquestion.history - {question.history}")
    answer = await chunk.async_summarize_question(dialog=question.text)
    return {"message": answer}
