import requests
import random
import time


url = 'http://localhost:5000/get-sensor-data'

def gerar_dados_sensor():
    temperatura = round(random.uniform(10, 30), 2)
    umidade = round(random.uniform(30, 90), 2)
    return temperatura, umidade

while True:
    temperatura, umidade = gerar_dados_sensor()

    response = requests.get(url, params={'temperatura': temperatura, 'umidade': umidade})

    if response.status_code == 200:
        print("Requisição enviada com sucesso")
    else:
        print("Erro ao enviar requisição")

   
    time.sleep(20)

