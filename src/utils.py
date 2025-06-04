import json
import logging
from typing import Any, Dict, List


def read_operations(file_path: str) -> List[Dict[str, Any]]:
    """Читает операции из JSON файла."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if not isinstance(data, list):
                logging.warning(f"File {file_path} does not contain a list")
                return []
            return data
    except FileNotFoundError:
        logging.error(f"File {file_path} not found")
        return []
    except json.JSONDecodeError:
        logging.error(f"File {file_path} contains invalid JSON")
        return []
    except Exception as e:
        logging.error(f"Unexpected error reading {file_path}: {e}")
        return []


def load_transactions(file_path: str) -> List[Dict[str, Any]]:
    """Загружает транзакции из файла."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"Error loading transactions: {e}")
        return []


def get_transaction_amount_rub(transaction: Dict[str, Any]) -> float:
    """Получает сумму транзакции в рублях."""
    try:
        from src.external_api import convert_to_rub
        return convert_to_rub(transaction)
    except ImportError:
        logging.error("Failed to import convert_to_rub function")
        raise
    except Exception as e:
        logging.error(f"Error getting transaction amount: {e}")
        raise