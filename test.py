import requests

# # использование кастомного chatgpt через кастомный api
# payload = {"text": "Расскажи про погоду?"}
# response = requests.post("http://127.0.0.1:5000/api/get_answer", json=payload)
# print(response.text)
#
# payload = {"text": "Расскажи что умеешь?"}
# response = requests.post("http://127.0.0.1:5000/api/get_answer", json=payload)
# print(response.text)
#
# payload = {"text": "Как определяется сумма страховых выплат?"}
# response = requests.post("http://127.0.0.1:5000/api/get_answer", json=payload)
# print(response.text)

payload = {"text": "Какие случаи подпадают под страховку?"}
response = requests.post("http://127.0.0.1:5000/api/get_answer", json=payload)
print(response.text)

# запросы в fastapi_example
response = requests.get("http://127.0.0.1:5000/count")
print(response.text)