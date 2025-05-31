"""Модуль для функциональности бэкенда банковского виджета."""
from datetime import datetime

from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(account_card_info: str) -> str:
    """Маскирует номер карты или счета в зависимости от типа."""
    if not account_card_info:
        raise ValueError("Строка не может быть пустой")

    parts = account_card_info.split()
    if len(parts) < 2:
        raise ValueError("Неверный формат строки")

    number = parts[-1]  # Последняя часть строки - это номер
    name = " ".join(parts[:-1])  # Все остальное - название

    if "Счет" in name:
        masked_number = get_mask_account(number)
    else:
        masked_number = get_mask_card_number(number)

    return f"{name} {masked_number}"


def get_date(date_str: str) -> str:
    """Преобразует дату из формата '2024-03-11T02:26:18.671407' в формат 'ДД.ММ.ГГГГ'."""
    date = datetime.fromisoformat(date_str)
    return date.strftime("%d.%m.%Y")
