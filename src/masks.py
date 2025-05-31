"""Маскировка банковских данных."""
from typing import Union


def get_mask_card_number(card_number: Union[int, str]) -> str:
    """Маскирует номер карты в формате XXXX XX** **** XXXX."""
    card_str = str(card_number)
    if len(card_str) != 16:
        raise ValueError("Номер карты должен содержать 16 цифр")
    if not card_str.isdigit():
        raise ValueError("Номер карты должен содержать только цифры")

    masked = f"{card_str[:4]} " f"{card_str[4:6]}** " f"**** " f"{card_str[-4:]}"
    return masked


def get_mask_account(account_number: Union[int, str]) -> str:
    """Маскирует номер счета в формате **XXXX."""
    account_str = str(account_number)
    if len(account_str) < 4:
        raise ValueError("Номер счета должен содержать как минимум 4 цифры")

    return f"**{account_str[-4:]}"
