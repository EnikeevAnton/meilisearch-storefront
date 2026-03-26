import os

import meilisearch
from dotenv import load_dotenv

load_dotenv()

MEILI_URL = os.getenv('MEILI_URL', 'http://localhost:7700')
MEILI_MASTER_KEY = os.getenv('MEILI_MASTER_KEY', 'masterKey')

client = meilisearch.Client(
    MEILI_URL, MEILI_MASTER_KEY if MEILI_MASTER_KEY else None
)


# количество результатов для тестов и демонстрации персонализации
# (можно менять)
TARGET_LIMIT = 5
