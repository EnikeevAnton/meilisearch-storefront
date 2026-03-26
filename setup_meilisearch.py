from config import client


def setup_indexes():
    configure_single_index('products')


def configure_single_index(index_name):
    print(f"Настройка индекса: {index_name}...")
    index = client.index(index_name)

    settings = {
        # поля для текстового поиска
        'searchableAttributes': [
            'title',
            'brand',
            'category',
            'tags',
            'description'
        ],

        # поля для фильтрации
        'filterableAttributes': [
            'brand',
            'category',
            'price',
            'rating'
        ],

        # поля для сортировки по возрастанию/убыванию
        'sortableAttributes': [
            'price',
            'rating'
        ],

        # отображаемые атрибуты (что возвращается в JSON-ответе)
        'displayedAttributes': [
            'id',
            'title',
            'description',
            'price',
            'brand',
            'category',
            'rating',
            'tags',
            'images'
        ]
    }

    task = index.update_settings(settings)
    print(f"Обновление {index_name} запущено. Task UID: {task.task_uid}")

    client.wait_for_task(task.task_uid)
    print("Настройки успешно применены!")


if __name__ == "__main__":
    setup_indexes()
