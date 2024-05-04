import json
import os
from datetime import datetime, timedelta
import requests
from dotenv import load_dotenv
from tabulate import tabulate

load_dotenv()
API_KEY = os.getenv('API_KEY')
URL = os.getenv('API_SERVER')
TABLE_FORMAT = os.getenv('TABLE_FORMAT')
headers = {
    'accept': 'application/json',
    'X-API-Key': API_KEY,
    'Content-Type': 'application/json'
}
table_data = []

response = requests.get(URL + 'services', headers=headers).json()
items = response.get('data').get('items')

def prolong_server(service_id, service_paymentTerm):
    prolong_url = f"{URL}services/{service_id}/prolong"
    data = {
        "method": "balance",
        "term": service_paymentTerm,
        "count": 1
    }
    response = requests.post(prolong_url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        response_data = response.json()
        if response_data.get('success', False):
            print(f"Сервис {service_id} успешно продлен.")
        else:
            error_message = response_data.get('message')
            if error_message:
                print(f"Ошибка продления сервиса {service_id}: {error_message}")
    elif response.status_code != 200:
        print(f"Ошибка продления сервиса {service_id}: {response.text}")

for item in items:
    service_id = item.get('id')
    service_name = item.get('name')
    service_paymentTerm = item.get('paymentTerm')
    service_expiresAt = datetime.fromtimestamp(
        item.get('timestamps').get('expiresAt')
    )

    if service_paymentTerm != 'month' != 'year' != 'half_year' != 'quarter_year':
        table_data.append([service_id, service_name, service_paymentTerm, service_expiresAt])

        # Расчет времени для продления сервера (за 23 часа до истечения срока действия)
        prolong_time = service_expiresAt - timedelta(hours=23)

        # Проверка, не нужно ли продлить сервер прямо сейчас
        if prolong_time <= datetime.now():
            try:
                prolong_server(service_id, service_paymentTerm)
            except Exception as e:
                print(f"Ошибка продления сервиса {service_id}: {str(e)}")
        else:
            # Не делать ничего, если продление не требуется
            pass

print(tabulate(table_data, headers=("ID", "Название услуги", "Тип оплаты услуги", "Истекает"), tablefmt=TABLE_FORMAT,
               stralign='center', numalign='center'))