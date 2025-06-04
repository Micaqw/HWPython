from unittest.mock import MagicMock, patch

import pytest

from src.external_api import convert_to_rub


@pytest.fixture
def sample_rub_transaction():
    """Фикстура с транзакцией в рублях."""
    return {
        "operationAmount": {
            "amount": "100.0",
            "currency": {
                "code": "RUB"
            }
        }
    }


@pytest.fixture
def sample_usd_transaction():
    """Фикстура с транзакцией в долларах."""
    return {
        "operationAmount": {
            "amount": "100.0",
            "currency": {
                "code": "USD"
            }
        }
    }


def test_convert_to_rub_already_in_rub(sample_rub_transaction):
    """Тест конвертации суммы, которая уже в рублях."""
    result = convert_to_rub(sample_rub_transaction)
    assert result == 100.0


@patch('src.external_api.os.getenv')
@patch('src.external_api.requests.get')
def test_convert_to_rub_from_usd(mock_get, mock_getenv, sample_usd_transaction):
    """Тест конвертации из USD в RUB."""
    mock_response = MagicMock()
    mock_response.json.return_value = {"result": 7500.0}
    mock_get.return_value = mock_response
    
    mock_getenv.return_value = "test_api_key"
    
    result = convert_to_rub(sample_usd_transaction)
    assert result == 7500.0
    
    mock_get.assert_called_once()
    args, kwargs = mock_get.call_args
    assert kwargs['params']['amount'] == "100.0"
    assert kwargs['params']['from'] == "USD"
    assert kwargs['params']['to'] == "RUB"
    assert kwargs['headers']['apikey'] == "test_api_key"


@patch('src.external_api.os.getenv')
def test_convert_to_rub_no_api_key(mock_getenv, sample_usd_transaction):
    """Тест ошибки при отсутствии API ключа."""
    mock_getenv.return_value = None
    with pytest.raises(ValueError, match="API key not found in environment variables"):
        convert_to_rub(sample_usd_transaction)


@patch('src.external_api.os.getenv')
@patch('src.external_api.requests.get')
def test_convert_to_rub_api_error(mock_get, mock_getenv, sample_usd_transaction):
    """Тест ошибки при запросе к API."""
    mock_getenv.return_value = "test_api_key"
    mock_get.side_effect = Exception("API Error")
    
    with pytest.raises(ValueError, match="Failed to convert currency"):
        convert_to_rub(sample_usd_transaction)


def test_convert_to_rub_invalid_transaction():
    """Тест невалидной структуры транзакции."""
    invalid_transactions = [
        {},
        {"operationAmount": {}},
        {"operationAmount": {"amount": "100.0"}},
        {"operationAmount": {"currency": {"code": "USD"}}},
    ]
    
    for transaction in invalid_transactions:
        with pytest.raises(ValueError):
            convert_to_rub(transaction) 