"""Тесты для модуля generators."""
import pytest
from src.generators import filter_by_currency, transaction_descriptions, card_number_generator


@pytest.fixture
def sample_transactions():
    """Фикстура с тестовыми данными транзакций."""
    return [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {
                "amount": "9824.07",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            },
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702"
        },
        {
            "id": 873106923,
            "state": "EXECUTED",
            "date": "2019-03-23T01:09:46.296404",
            "operationAmount": {
                "amount": "43318.34",
                "currency": {
                    "name": "руб.",
                    "code": "RUB"
                }
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 44812258784861134719",
            "to": "Счет 74489636417521191160"
        }
    ]


class TestFilterByCurrency:
    """Тесты для функции filter_by_currency."""

    @pytest.mark.parametrize("currency,expected_count", [
        ("USD", 1),
        ("RUB", 1),
        ("EUR", 0)
    ])
    def test_filter_by_currency(self, sample_transactions, currency, expected_count):
        """Проверяет корректность фильтрации по валюте."""
        filtered = list(filter_by_currency(sample_transactions, currency))
        assert len(filtered) == expected_count
        if expected_count > 0:
            assert all(t["operationAmount"]["currency"]["code"] == currency for t in filtered)

    def test_empty_transactions(self):
        """Проверяет работу с пустым списком транзакций."""
        filtered = list(filter_by_currency([], "USD"))
        assert len(filtered) == 0


class TestTransactionDescriptions:
    """Тесты для функции transaction_descriptions."""

    def test_descriptions_generator(self, sample_transactions):
        """Проверяет корректность генерации описаний."""
        descriptions = list(transaction_descriptions(sample_transactions))
        assert len(descriptions) == 2
        assert descriptions[0] == "Перевод организации"
        assert descriptions[1] == "Перевод со счета на счет"

    def test_empty_transactions(self):
        """Проверяет работу с пустым списком транзакций."""
        descriptions = list(transaction_descriptions([]))
        assert len(descriptions) == 0


class TestCardNumberGenerator:
    """Тесты для функции card_number_generator."""

    @pytest.mark.parametrize("start,stop,expected", [
        (1, 3, [
            "0000 0000 0000 0001",
            "0000 0000 0000 0002",
            "0000 0000 0000 0003"
        ]),
        (9998, 9999, [
            "0000 0000 0000 9998",
            "0000 0000 0000 9999"
        ])
    ])
    def test_card_number_generation(self, start, stop, expected):
        """Проверяет корректность генерации номеров карт."""
        numbers = list(card_number_generator(start, stop))
        assert numbers == expected

    def test_card_number_format(self):
        """Проверяет формат генерируемых номеров карт."""
        number = next(card_number_generator(1, 1))
        assert len(number) == 19  # 16 цифр + 3 пробела
        assert number.count(" ") == 3
        assert all(c.isdigit() or c.isspace() for c in number) 