# Знакомство с Meilisearch

## Набор данных

В качестве источника данных используется публичный API [DummyJSON](https://dummyjson.com/products). Скрипт загрузки автоматически обращается к эндпоинту и скачивает массив товаров.

**Пример структуры получаемого объекта (один товар):**

```json
{
  "products": [
    {
      "id": 1,
      "title": "Essence Mascara Lash Princess",
      "description": "The Essence Mascara Lash Princess is a popular mascara known for its volumizing and lengthening effects. Achieve dramatic lashes with this long-lasting and cruelty-free formula.",
      "category": "beauty",
      "price": 9.99,
      "discountPercentage": 10.48,
      "rating": 2.56,
      "stock": 99,
      "tags": [
        "beauty",
        "mascara"
      ],
      "brand": "Essence",
      "sku": "BEA-ESS-ESS-001",
      "weight": 4,
      "dimensions": {
        "width": 15.14,
        "height": 13.08,
        "depth": 22.99
      },
      "warrantyInformation": "1 week warranty",
      "shippingInformation": "Ships in 3-5 business days",
      "availabilityStatus": "In Stock",
      "reviews": [
        {
          "rating": 3,
          "comment": "Would not recommend!",
          "date": "2025-04-30T09:41:02.053Z",
          "reviewerName": "Eleanor Collins",
          "reviewerEmail": "eleanor.collins@x.dummyjson.com"
        }
      ],
      "returnPolicy": "No return policy",
      "minimumOrderQuantity": 48,
      "meta": {
        "createdAt": "2025-04-30T09:41:02.053Z",
        "updatedAt": "2025-04-30T09:41:02.053Z",
        "barcode": "5784719087687",
        "qrCode": "[https://cdn.dummyjson.com/public/qr-code.png](https://cdn.dummyjson.com/public/qr-code.png)"
      },
      "images": [
        "[https://cdn.dummyjson.com/product-images/beauty/essence-mascara-lash-princess/1.webp](https://cdn.dummyjson.com/product-images/beauty/essence-mascara-lash-princess/1.webp)"
      ],
      "thumbnail": "[https://cdn.dummyjson.com/product-images/beauty/essence-mascara-lash-princess/thumbnail.webp](https://cdn.dummyjson.com/product-images/beauty/essence-mascara-lash-princess/thumbnail.webp)"
    }
  ]
}
```

## Как запустить и воспроизвести результат

### 1. Требования

- **Docker** (для запуска сервера Meilisearch)
- **Python 3.9+**

### 2. Подготовка

Клонируйте репозиторий и перейдите в папку проекта:

```bash
git clone https://github.com/EnikeevAnton/meilisearch-storefront.git
cd meilisearch-storefront
```

Создайте `.env` на основе примера:

```bash
cp .env.example .env
```

### 3. Запуск Meilisearch
Поднимите контейнер:
```bash
docker compose up --build -d
```

Проверьте, что сервис доступен:

```bash
curl http://127.0.0.1:7700/health
```

### 4. Установка зависимостей Python

Создайте и активируйте виртуальное окружение, а затем установите необходимые библиотеки:

Для Linux/macOS:
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
Для Windows:

```Bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```
### 5. Настройка индекса
Перед загрузкой данных необходимо настроить правила работы поискового движка

```Bash
python setup_meilisearch.py
```
**Что делает скрипт:**
Скрипт создает индекс `products` и применяет следующие настройки:

- `searchableAttributes`: ограничивает полнотекстовый поиск только по полям `title`, `brand`, `category`, `tags`, `description`.

- `filterableAttributes`: разрешает фильтрацию по полям `brand`, `category`, `price`, `rating`.

- `sortableAttributes`: включает возможность сортировки по `price` и `rating`.

### 6. Импорт данных
Скачайте данные из API и отправьте их в подготовленный индекс:

```Bash
python load_data.py
```
*Скрипт скачает 200 товаров с DummyJSON, загрузит их батчем в Meilisearch и дождется успешного статуса выполнения задачи (Task Status: `succeeded`).*

> **Визуальная проверка данных:**
> После завершения импорта вы можете просмотреть базу данных через встроенный веб-интерфейс Meilisearch.
>
> 1.  Откройте в браузере: [http://localhost:7700](http://localhost:7700)
> 2.  Введите ключ доступа (Master Key): `masterKey` *(или тот, что указан в вашем файле `.env`)*.
>
> В интерфейсе можно в реальном времени протестировать поиск и посмотреть структуру документов.

### 7. Проверка работы поиска (Тестовые сценарии)
Для проверки работоспособности базовых функций движка запустите скрипт:

```Bash
python test_search.py
```
Скрипт выполнит ряд проверочных сценариев и сохранит полные ответы сервера в папку `test_results/` в формате JSON-файлов. 

Ниже приведены 4 ключевых сценария, которые тестирует данный скрипт:
### Сценарий 1: Простой полнотекстовый поиск по ключевому слову
* **Параметры:** `query: "mascara"`
* **Суть проверки:** Убедиться, что базовый текстовый поиск работает корректно. Движок ищет совпадения слова "mascara" по всем полям, которые мы явно указали в настройке `searchableAttributes` (например, в названиях и описаниях товаров).

### Сценарий 2: Поиск с фильтром по конкретному значению поля
* **Параметры:** `query: ""`, `filter: ["category = 'beauty'"]`
* **Суть проверки:** Проверить работу фильтрации по строковому значению (строгое совпадение). Успешное выполнение запроса подтверждает, что поле `category` было правильно добавлено в `filterableAttributes` на этапе настройки индекса.

### Сценарий 3: Поиск с фильтром по числовому диапазону
* **Параметры:** `query: ""`, `filter: ["price >= 20 AND price <= 50"]`
* **Суть проверки:** Проверить способность движка обрабатывать математические операторы и логическое 'И' (`AND`). Запрос отбирает только те товары, цена которых находится строго в заданном коридоре от 20 до 50. Это подтверждает, что поле `price` проиндексировано как числовое и доступно для фильтрации.

### Сценарий 4: Сортировка результатов по числовому полю (по возрастанию и по убыванию)
* **Параметры 4а (по возрастанию):** `query: ""`, `sort: ["price:asc"]`
* **Параметры 4б (по убыванию):** `query: ""`, `sort: ["price:desc"]`
* **Суть проверки:** Убедиться, что пользовательская сортировка работает в обоих направлениях (от дешевых к дорогим и наоборот).

### 8. Персонализация выдачи
В проекте реализован алгоритм персонализации поисковой выдачи на основе истории взаимодействия пользователя, работающий без сложных алгоритмов. 

Для запуска демонстрации выполните:

```Bash
python personalization.py
```
После запуска в терминале появится **интерактивное меню**. Вы можете протестировать систему на заготовленных сценариях или ввести собственный текст:
* `1`, `2`, `3`, `4` — Заготовленные запросы (`luxurious`, `popular`, `red`, `classic`), демонстрирующие разные уровни совпадения истории пользователя и поисковой выдачи.
* `5` — Пустой запрос `""`
* `6` — Ввести любой свой поисковый запрос.
* `0` — Выход.

Результаты выполнения в формате JSON будут сохранены в папку `personalization_results/` (при каждом новом запросе данные перезаписываются).


### Пример входных данных (История пользователя)
Допустим, мы знаем, что пользователь ранее просматривал товары определенных брендов и категорий. Эти данные зафиксированы:

```json
{
    "viewed_brands": ["Essence", "Dior"],
    "viewed_categories": ["beauty", "fragrances"]
}
```

### Сравнение выдачи с персонализацией и без
Запрос: `query: "red"`, `sort: ["rating:desc"]`

**Выдача БЕЗ персонализации (Стандартный поиск):**
Движок ищет слово "red" и возвращает результаты, опираясь исключительно на внутренние правила текстовой релевантности (совпадения в названии, описании и т.д.).
1. Nike Air Jordan 1 Red And Black | Бренд: Nike | Категория: mens-shoes | ★ 4.77
2. Sports Sneakers Off White & Red | Бренд: Off White | Категория: mens-shoes | ★ 4.77
3. Sports Sneakers Off White Red | Бренд: Off White | Категория: mens-shoes | ★ 4.69
4. Marni Red & Black Suit | Бренд: Без бренда | Категория: womens-dresses | ★ 4.48
5. Red Tongs | Бренд: Без бренда | Категория: kitchen-accessories | ★ 4.42 

**Выдача С персонализацией:**
Алгоритм выводит на первые места товары, соответствующие профилю пользователя, а затем добивает ленту обычными результатами.
1. [Рекомендация]      Red Lipstick | Бренд: Chic Cosmetics | Категория: beauty | ★ 4.36
2. [Рекомендация]      Red Nail Polish | Бренд: Nail Couture | Категория: beauty | ★ 4.32
3. [Общая выдача]      Nike Air Jordan 1 Red And Black | Бренд: Nike | Категория: mens-shoes | ★ 4.77
4. [Общая выдача]      Sports Sneakers Off White & Red | Бренд: Off White | Категория: mens-shoes | ★ 4.77
5. [Общая выдача]      Sports Sneakers Off White Red | Бренд: Off White | Категория: mens-shoes | ★ 4.69

### Почему результаты отличаются (Комментарий)
Результаты отличаются, потому что в персонализированной версии мы перехватываем запрос и разбиваем его на два этапа:

1. **Приоритетная выборка:** Сначала мы ищем товары по запросу `"red"`, но накладываем фильтр по профилю пользователя: `brand IN ['Essence', 'Dior'] OR category IN ['beauty', 'fragrances']`. Чтобы наверх попали самые лучшие товары, мы применяем сортировку `sort: ['rating:desc']`.
2. **Дополнение :** Если приоритетных товаров не хватило для заполнения лимита (например, найдено только 2 из 5), мы делаем второй запрос к базе с обратным фильтром `NOT IN`, чтобы получить остальные товары и заполнить пустые места в выдаче.

В результате мы получаем персонализированную ленту (комбинацию двух склеенных запросов), которая показывает пользователю релевантные его интересам товары, но при этом не скрывает от него остальной каталог магазина.

> **Масштабирование выдачи (TARGET_LIMIT)**
> Размер итоговой ленты товаров (в данном примере это 5 элементов) регулируется глобальной переменной `TARGET_LIMIT` в файле `config.py`. Вы можете изменить это значение (например, на 20 или 50).
