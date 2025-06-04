import json
import os
import sys
from unittest.mock import patch

import pytest


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.utils import get_transaction_amount_rub, load_transactions, read_operations


@pytest.fixture
def sample_operations():
    return [
        {
            "id": 1,
            "operationAmount": {
                "amount": "100.0",
                "currency": {
                    "code": "RUB"
                }
            }
        }
    ]

def test_get_transaction_amount_rub_rub():
    """Тест конвертации рублевой транзакции."""
    transaction = {
        'operationAmount': {
            'amount': '100.0',
            'currency': {
                'code': 'RUB'
            }
        }
    }
    assert get_transaction_amount_rub(transaction) == 100.0

@patch('src.utils.convert_to_rub')
def test_get_transaction_amount_rub_foreign(mock_convert_to_rub):
    """Тест конвертации валютной транзакции."""
    mock_convert_to_rub.return_value = 4500.0
    transaction = {
        'operationAmount': {
            'amount': '25.0',
            'currency': {
                'code': 'EUR'
            }
        }
    }
    assert get_transaction_amount_rub(transaction) == 4500.0
    mock_convert_to_rub.assert_called_once()

@patch('src.utils.convert_to_rub')
def test_get_transaction_amount_rub_conversion_failure(mock_convert_to_rub):
    """Тест ошибки конвертации."""
    mock_convert_to_rub.return_value = None
    transaction = {
        'operationAmount': {
            'amount': '25.0',
            'currency': {
                'code': 'EUR'
            }
        }
    }
    with pytest.raises(ValueError):
        get_transaction_amount_rub(transaction)

def test_get_transaction_amount_rub_invalid_input():
    """Тест невалидного ввода."""
    with pytest.raises(ValueError):
        get_transaction_amount_rub({})
    with pytest.raises(ValueError):
        get_transaction_amount_rub({'operationAmount': {'currency': {'code': 'RUB'}}})

def test_load_transactions(tmp_path):
    """Тест загрузки транзакций из файла"""
    test_file = tmp_path / "test.json"
    test_data = [{"id": 1, "amount": 100}]
    
    with open(test_file, 'w', encoding='utf-8') as f:
        json.dump(test_data, f)
    
    result = load_transactions(str(test_file))
    assert result == test_data

def test_read_operations_success(tmp_path, sample_operations):
    """Тест успешного чтения JSON-файла."""
    test_file = tmp_path / "operations.json"
    with open(test_file, 'w', encoding='utf-8') as f:
        json.dump(sample_operations, f)
    result = read_operations(str(test_file))
    assert result == sample_operations

def test_read_operations_empty_file(tmp_path):
    """Тест чтения пустого файла."""
    empty_file = tmp_path / "empty.json"
    with open(empty_file, 'w', encoding='utf-8') as f:
        f.write("")
    assert read_operations(str(empty_file)) == []

def test_read_operations_invalid_json(tmp_path):
    """Тест чтения невалидного JSON."""
    invalid_file = tmp_path / "invalid.json"
    with open(invalid_file, 'w', encoding='utf-8') as f:
        f.write("{invalid json}")
    assert read_operations(str(invalid_file)) == []

def test_read_operations_not_list(tmp_path):
    """Тест чтения JSON-файла с не-списком."""
    not_list_file = tmp_path / "not_list.json"
    with open(not_list_file, 'w', encoding='utf-8') as f:
        json.dump({"key": "value"}, f)
    assert read_operations(str(not_list_file)) == []

def test_read_operations_file_not_found():
    """Тест чтения несуществующего файла."""
    assert read_operations("nonexistent.json") == [] 