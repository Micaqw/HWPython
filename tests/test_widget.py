import pytest
from src.widget import mask_account_card, get_date


@pytest.mark.parametrize("input_str,expected", [
    ("Счет 35158586384610753655", "Счет **3655"),
    ("Visa Classic 2842878893689012", "Visa Classic 2842 87** **** 9012"),
    ("Maestro 3928549031574026", "Maestro 3928 54** **** 4026"),
])
def test_mask_account_card_valid(input_str: str, expected: str) -> None:
    """Тест маскировки валидных номеров карт и счетов"""
    assert mask_account_card(input_str) == expected


@pytest.mark.parametrize("invalid_input", [
    "Счет 123",  # слишком короткий номер счета
    "Visa Classic 12345",  # неверный формат номера карты
    "",  # пустая строка
])
def test_mask_account_card_invalid(invalid_input: str) -> None:
    """Тест маскировки невалидных номеров карт и счетов"""
    with pytest.raises(ValueError):
        mask_account_card(invalid_input)


@pytest.mark.parametrize("date_str,expected", [
    ("2024-03-11T02:26:18.671407", "11.03.2024"),
    ("2024-03-10T02:26:18.671407", "10.03.2024"),
    ("2024-03-09T02:26:18.671407", "09.03.2024"),
])
def test_get_date_valid(date_str: str, expected: str) -> None:
    """Тест преобразования валидных дат"""
    assert get_date(date_str) == expected


@pytest.mark.parametrize("invalid_date", [
    "2024-13-11T02:26:18.671407",  # неверный месяц
    "2024-03-32T02:26:18.671407",  # неверный день
    "invalid_date",  # неверный формат
    "",  # пустая строка
])
def test_get_date_invalid(invalid_date: str) -> None:
    """Тест преобразования невалидных дат"""
    with pytest.raises(ValueError):
        get_date(invalid_date)
