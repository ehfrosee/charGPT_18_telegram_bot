from fastapi import FastAPI
from chunks import Chunk
import openai
from pydantic import BaseModel
from dotenv import load_dotenv

#uvicorn main:app --port 5000

# инициализация индексной базы
data_url = 'https://docs.google.com/document/d/11MU3SnVbwL_rM-5fIC14Lc3XnbAV4rY1Zd_kpcMuH4Y'
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
    answer = chunk.get_answer(query=question.text)
    return {"message": answer}

