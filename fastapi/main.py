from fastapi import FastAPI
from chunks import Chunk
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

# инициализация индексной базы
chunk = Chunk(path_to_base="Simble.txt")

# класс с типами данных параметров 
class Item(BaseModel): 
    text: str

# создаем объект приложения
app = FastAPI()
app.count = 0

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

# функция обработки post запроса + декоратор 
@app.post("/api/get_answer")
def get_answer(question: Item):
    answer = chunk.get_answer(query=question.text)
    return {"message": answer}

# функция обработки get запроса для подсчета количества обращений
@app.get("/api/num_requests")
def read_root():
    app.count = app.count + 1
    return {"num_requests": app.count}