import json
import os
from config import client, TARGET_LIMIT

index = client.index('products')

# папка для сохранения результатов тестов
RESULTS_DIR = 'test_results'
os.makedirs(RESULTS_DIR, exist_ok=True)


def save_and_print_summary(scenario_name, filename, results):
    print(f"\n{'-'*10} {scenario_name} {'-'*10}")

    hits = results.get('hits', [])
    processing_time = results.get('processingTimeMs', 0)
    total_hits = results.get('estimatedTotalHits', len(hits))

    print(f"Всего совпадений в базе: {total_hits}")
    print(
        f"Загружено по лимиту: {len(hits)} (Время выполнения: {processing_time} мс)")
    filepath = os.path.join(RESULTS_DIR, filename)

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"Результаты сохранены в: {filepath}")


def run_scenarios():
    print("Запуск проверочных сценариев Meilisearch...")

    # Сценарий 1: Простой полнотекстовый поиск по ключевому слову
    res_text = index.search('mascara', {
        'limit': TARGET_LIMIT
    })
    save_and_print_summary(
        "Сценарий 1: Поиск 'mascara'",
        "1_search_keyword_mascara.json",
        res_text
    )

    # Сценарий 2: Поиск с фильтром по конкретному значению поля
    res_filter_exact = index.search('', {
        'filter': ["category = 'beauty'"],
        'limit': TARGET_LIMIT
    })
    save_and_print_summary(
        "Сценарий 2: Фильтр category = 'beauty'",
        "2_filter_category_beauty.json",
        res_filter_exact
    )

    # Сценарий 3: Поиск с фильтром по числовому диапазону
    res_filter_range = index.search('', {
        'filter': ['price >= 20 AND price <= 50'],
        'limit': TARGET_LIMIT
    })
    save_and_print_summary(
        "Сценарий 3: Фильтр цены ($20 - $50)",
        "3_filter_price_range_20_50.json",
        res_filter_range
    )

    # Сценарий 4 (а): Сортировка результатов по числовому полю (по возрастанию)
    res_sort_asc = index.search('', {
        'sort': ['price:asc'],
        'limit': TARGET_LIMIT
    })
    save_and_print_summary(
        "Сценарий 4а: Сортировка цены по возрастанию",
        "4a_sort_price_asc.json",
        res_sort_asc
    )

    # Сценарий 4 (б): Сортировка результатов по числовому полю (по убыванию)
    res_sort_desc = index.search('', {
        'sort': ['price:desc'],
        'limit': TARGET_LIMIT
    })
    save_and_print_summary(
        "Сценарий 4б: Сортировка цены по убыванию",
        "4b_sort_price_desc.json",
        res_sort_desc
    )


if __name__ == "__main__":
    run_scenarios()
