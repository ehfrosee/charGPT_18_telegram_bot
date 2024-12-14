from fastapi import FastAPI
from chunks import Chunk
from pydantic import BaseModel
from langchain_core.pydantic_v1 import BaseModel
# uvicorn main:app --port 5000

# инициализация индексной базы
data_url = 'data.txt'
chunk = Chunk(path_to_base=data_url)


# класс с типами данных параметров
class Item(BaseModel):
    text: str


# создаем объект приложения
app = FastAPI()


# функция обработки get запроса + декоратор
@app.get("/")
def read_root():
    return {"message": "answer"}


# функция обработки post запроса + декоратор
@app.post("/api/get_answer")
def get_answer(question: Item):
    pass
    answer = chunk.get_answer(query=question.text)
    return {"message": answer}
