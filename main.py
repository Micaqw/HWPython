"""Основной модуль для демонстрации работы банковского виджета."""
from src.widget import get_date, mask_account_card


def main() -> None:
    """Демонстрация работы функций маскировки."""
    # Примеры маскировки карт и счетов
    test_data = [
        "Maestro 1596837868705199",
        "Счет 64686473678894779589",
        "MasterCard 7158300734726758",
        "Счет 35383033474447895560",
        "Visa Classic 6831982476737658",
        "Visa Platinum 8990922113665229",
        "Visa Gold 5999414228426353",
        "Счет 73654108430135874305",
    ]

    print("Тестирование функции mask_account_card:")
    for data in test_data:
        masked = mask_account_card(data)
        print(f"{data} -> {masked}")

    print("\nТестирование функции get_date:")
    test_date = "2024-03-11T02:26:18.671407"
    formatted_date = get_date(test_date)
    print(f"{test_date} -> {formatted_date}")


if __name__ == "__main__":
    main()
