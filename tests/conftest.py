import pytest
from typing import List, Dict


@pytest.fixture
def sample_operations() -> List[Dict]:
    """Фикстура с тестовыми данными операций"""
    return [
        {
            "id": 1,
            "state": "EXECUTED",
            "date": "2024-03-11T02:26:18.671407",
            "operationAmount": {"amount": "31957.58", "currency": {"name": "руб.", "code": "RUB"}},
            "description": "Перевод организации",
            "from": "Visa Classic 2842878893689012",
            "to": "Счет 35158586384610753655"
        },
        {
            "id": 2,
            "state": "CANCELED",
            "date": "2024-03-10T02:26:18.671407",
            "operationAmount": {"amount": "50870.71", "currency": {"name": "руб.", "code": "RUB"}},
            "description": "Перевод с карты на карту",
            "from": "Maestro 3928549031574026",
            "to": "Visa Classic 4195191172583802"
        },
        {
            "id": 3,
            "state": "EXECUTED",
            "date": "2024-03-09T02:26:18.671407",
            "operationAmount": {"amount": "21344.35", "currency": {"name": "руб.", "code": "RUB"}},
            "description": "Открытие вклада",
            "to": "Счет 77613226829885488381"
        }
    ]


@pytest.fixture
def sample_card_numbers() -> List[str]:
    """Фикстура с тестовыми номерами карт"""
    return [
        "2842878893689012",  # Valid 16-digit number
        "123456789012345",   # 15-digit number (invalid)
        "28428788936890123"  # 17-digit number (invalid)
    ]


@pytest.fixture
def sample_account_numbers() -> List[str]:
    """Фикстура с тестовыми номерами счетов"""
    return [
        "35158586384610753655",  # Valid account number
        "123",                   # Too short (invalid)
        "1234567890"            # Valid account number
    ]


@pytest.fixture
def sample_dates() -> List[str]:
    """Фикстура с тестовыми датами"""
    return [
        "2024-03-11T02:26:18.671407",
        "2024-03-10T02:26:18.671407",
        "2024-03-09T02:26:18.671407"
    ]
