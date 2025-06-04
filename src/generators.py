"""
Модуль для работы с генераторами транзакций.

Содержит функции для фильтрации и обработки транзакций,
а также генерации номеров банковских карт.
"""
from typing import Dict, Generator, Iterator, List


def filter_by_currency(transactions: List[Dict], currency: str) -> Iterator[Dict]:
    """Фильтрует транзакции по заданной валюте."""
    for transaction in transactions:
        if transaction['operationAmount']['currency']['code'] == currency:
            yield transaction


def transaction_descriptions(transactions: List[Dict]) -> Generator[str, None, None]:
    """Генерирует описания транзакций."""
    for transaction in transactions:
        yield transaction['description']


def card_number_generator(start: int, stop: int) -> Generator[str, None, None]:
    """Генерирует номера банковских карт в заданном диапазоне."""
    for number in range(start, stop + 1):
        # Преобразуем число в 16-значную строку с ведущими нулями
        card_number = str(number).zfill(16)
        # Форматируем строку, добавляя пробелы каждые 4 символа
        formatted_number = ' '.join(card_number[i:i+4] for i in range(0, 16, 4))
        yield formatted_number 