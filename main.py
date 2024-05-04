import requests
import os

from tabulate import tabulate
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('API_KEY')
URL = os.getenv('BASE_ENDPOINT')
TABLE_FORMAT = os.getenv('TABLE_FORMAT')

headers = {
	'accept': 'application/json',
	'X-API-Key': API_KEY,
}

response = requests.get(URL + '/services', headers = headers)
results = response.json()

items = results.get('data').get('items')
timestamps = items.get('timestamps')
print(timestamps)
table_data = []

for item in items:
	id = item.get('id')
	name = item.get('name')
	paymentTerm = item.get('paymentTerm')
	# timestamps = timestamps.get('expiresAt')
	
	table_data.append([id, name, paymentTerm, timestamps])

print(tabulate(table_data, headers = ['ID', 'Название услуги', 'Тип оплаты сервера', 'Истекает'], tablefmt = TABLE_FORMAT))