import json
import os
from config import client, TARGET_LIMIT

index = client.index('products')

RESULTS_DIR = 'personalization_results'
os.makedirs(RESULTS_DIR, exist_ok=True)


# история взаимодействия пользователя
user_history = {
    "viewed_brands": ["Essence", "Dior"],
    "viewed_categories": ["beauty", "fragrances"]
}


def save_json(filename, data):
    filepath = os.path.join(RESULTS_DIR, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return filepath


def demonstrate_personalization(query="classic"):
    print(
        f"\nПоисковый запрос: '{query}', сортировка по убыванию рейтинга (rating:desc)")
    print("=" * 70)

    # выдача без персонализации (стандартный поиск)
    res_standard = index.search(query, {'limit': TARGET_LIMIT})
    standard_hits = res_standard.get('hits', [])
    save_json("1_standard_results.json", res_standard)

    print("\n[ ВЫДАЧА БЕЗ ПЕРСОНАЛИЗАЦИИ ]")
    for i, item in enumerate(standard_hits, 1):
        brand = item.get('brand', 'Без бренда')
        category = item.get('category', 'Без категории')
        print(
            f"{i}. {item['title']} | Бренд: {brand} | Категория: {category} | ★ {item.get('rating')}")

    # персонализированная выдача
    brands_str = ", ".join([f"'{b}'" for b in user_history['viewed_brands']])
    cats_str = ", ".join([f"'{c}'" for c in user_history['viewed_categories']])

    filter_history = f"brand IN [{brands_str}] OR category IN [{cats_str}]"
    filter_others = f"brand NOT IN [{brands_str}] AND category NOT IN [{cats_str}]"

    # пробуем заполнить весь лимит (TARGET_LIMIT) персонализированными товарами
    res_history = index.search(query, {
        'filter': [filter_history],
        'sort': ['rating:desc'],
        'limit': TARGET_LIMIT
    })

    personalized_hits = res_history.get('hits', [])
    fallback_hits = []
    personalized_count = len(personalized_hits)
    # проверяем, нужно ли дополнять выдачу обычными товарами
    if len(personalized_hits) < TARGET_LIMIT:
        remaining_limit = TARGET_LIMIT - personalized_count

        # делаем второй запрос только на недостающее количество
        res_others = index.search(query, {
            'filter': [filter_others],
            'sort': ['rating:desc'],
            'limit': remaining_limit
        })
        fallback_hits = res_others.get('hits', [])
        personalized_hits.extend(fallback_hits)

    # сохраняем итоговый результат в один файл
    save_json("2_personalized_results.json", {
        "metadata": {
            "target_limit": TARGET_LIMIT,
            "personalized_count": personalized_count,
            "fallback_count": len(fallback_hits)
        },
        "user_profile": user_history,
        "hits": personalized_hits
    })

    print(f"\n[ ПЕРСОНАЛИЗИРОВАННАЯ ВЫДАЧА ]")
    print(
        f"История пользовтеля: Бренды {user_history['viewed_brands']} | Категории {user_history['viewed_categories']}")
    print("-" * 70)

    for i, item in enumerate(personalized_hits, 1):
        brand = item.get('brand', 'Без бренда')
        category = item.get('category', 'Без категории')
        rating = item.get('rating', 0)

        is_fav_brand = brand in user_history['viewed_brands']
        is_fav_cat = category in user_history['viewed_categories']

        if is_fav_brand and is_fav_cat:
            marker = "[Полное совпадение]"
        elif is_fav_brand or is_fav_cat:
            marker = "[Рекомендация]     "
        else:
            marker = "[Общая выдача]     "

        print(
            f"{i}. {marker} {item['title']} | Бренд: {brand} | Категория: {category} | ★ {rating}")

    print("\n" + "=" * 70)
    print(f"Файлы сохранены в 'personalization_results/'")
    print(
        f"Статистика: Найдено товаров: {len(res_history.get('hits', []))}, персонализированно: {personalized_count}")


if __name__ == "__main__":
    demonstrate_personalization()
