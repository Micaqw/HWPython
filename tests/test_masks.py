import pytest
from typing import Union
from src.masks import get_mask_card_number, get_mask_account


@pytest.mark.parametrize("card_number,expected", [
    ("2842878893689012", "2842 87** **** 9012"),
    (2842878893689012, "2842 87** **** 9012"),
])
def test_get_mask_card_number_valid(card_number: Union[str, int], expected: str) -> None:
    """Тест маскировки валидных номеров карт"""
    assert get_mask_card_number(card_number) == expected


@pytest.mark.parametrize("invalid_card", [
    "123456789012345",  # 15 digits
    "12345678901234567",  # 17 digits
    "abcdefghijklmnop",  # not numeric
    "",  # empty string
])
def test_get_mask_card_number_invalid(invalid_card: str) -> None:
    """Тест маскировки невалидных номеров карт"""
    with pytest.raises(ValueError):
        get_mask_card_number(invalid_card)


@pytest.mark.parametrize("account_number,expected", [
    ("35158586384610753655", "**3655"),
    (35158586384610753655, "**3655"),
    ("1234567890", "**7890"),
])
def test_get_mask_account_valid(account_number: Union[str, int], expected: str) -> None:
    """Тест маскировки валидных номеров счетов"""
    assert get_mask_account(account_number) == expected


@pytest.mark.parametrize("invalid_account", [
    "123",  # too short
    "",  # empty string
])
def test_get_mask_account_invalid(invalid_account: str) -> None:
    """Тест маскировки невалидных номеров счетов"""
    with pytest.raises(ValueError):
        get_mask_account(invalid_account)
