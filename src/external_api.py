import logging
import os
from typing import Any, Dict

import requests
from dotenv import load_dotenv


# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Загрузка переменных окружения
load_dotenv()


def validate_transaction(transaction: Dict[str, Any]) -> None:
    """Проверяет корректность структуры транзакции."""
    if not isinstance(transaction, dict):
        raise ValueError("Transaction must be a dictionary")

    if 'operationAmount' not in transaction:
        raise ValueError("Transaction must have 'operationAmount' key")

    operation_amount = transaction['operationAmount']
    if not isinstance(operation_amount, dict):
        raise ValueError("operationAmount must be a dictionary")

    if 'amount' not in operation_amount:
        raise ValueError("Transaction must have 'amount' in operationAmount")

    if 'currency' not in operation_amount:
        raise ValueError("Transaction must have 'currency' in operationAmount")

    if not isinstance(operation_amount['currency'], dict):
        raise ValueError("Currency must be a dictionary")

    if 'code' not in operation_amount['currency']:
        raise ValueError("Transaction must have 'code' in currency")


def get_exchange_rate(from_currency: str, to_currency: str = 'RUB', amount: float = 1.0) -> float:
    """Получает курс обмена валют."""
    api_key = os.getenv('EXCHANGE_API_KEY')
    if not api_key:
        logging.error("API key not found in environment variables")
        raise ValueError("API key not found in environment variables")

    base_url = "https://api.apilayer.com/exchangerates_data/convert"
    params = {
        "from": from_currency,
        "to": to_currency,
        "amount": str(amount)
    }
    headers = {"apikey": api_key}

    try:
        response = requests.get(
            base_url,
            params=params,
            headers=headers,
            timeout=10
        )
        response.raise_for_status()
        result = response.json()
        if 'result' not in result:
            raise ValueError("Invalid API response format")
        return float(result['result'])
    except requests.Timeout:
        logging.error("Timeout error while converting currency")
        raise ValueError("Failed to convert currency: timeout")
    except requests.RequestException as e:
        logging.error(f"Network error while converting currency: {e}")
        raise ValueError("Failed to convert currency: network error")
    except (KeyError, ValueError) as e:
        logging.error(f"Invalid API response: {e}")
        raise ValueError("Failed to convert currency: invalid response")
    except Exception as e:
        logging.error(f"Unexpected error while converting currency: {e}")
        raise ValueError("Failed to convert currency: unexpected error")


def convert_to_rub(transaction: Dict[str, Any]) -> float:
    """Конвертирует сумму транзакции в рубли."""
    validate_transaction(transaction)

    amount = float(transaction['operationAmount']['amount'])
    currency = transaction['operationAmount']['currency']['code']

    if amount < 0:
        raise ValueError("Amount cannot be negative")

    if currency == 'RUB':
        return amount

    try:
        converted_amount = get_exchange_rate(currency, 'RUB', amount)
        logging.info(f"Successfully converted {amount} {currency} to {converted_amount} RUB")
        return converted_amount
    except ValueError as e:
        logging.error(f"Failed to convert {amount} {currency} to RUB: {e}")
        raise

