import requests
from config import client


def load_products():
    print("1. Загружаем данные с DummyJSON...")
    url = 'https://dummyjson.com/products?limit=200'

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        products = data.get('products', [])
        print(f"Успешно скачано {len(products)} товаров.")

    except requests.exceptions.RequestException as e:
        print(f"Ошибка при скачивании данных: {e}")
        return

    print("2. Загружаем документы в Meilisearch...")
    index = client.index('products')

    task = index.add_documents(products)
    print(f"Задача на добавление создана. Task UID: {task.task_uid}")

    print("Ожидаем завершения индексации...")
    client.wait_for_task(task.task_uid)

    print("Все товары успешно загружены в индекс.")


if __name__ == "__main__":
    load_products()
