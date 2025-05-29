from typing import List, Dict, Union
from datetime import datetime


def filter_by_state(operations: List[Dict], state: str = 'EXECUTED') -> List[Dict]:
    """
    Фильтрует список операций по статусу.

    Args:
        operations: Список словарей с банковскими операциями
        state: Статус операции для фильтрации (по умолчанию 'EXECUTED')

    Returns:
        List[Dict]: Отфильтрованный список операций с указанным статусом
    """
    return [operation for operation in operations if operation.get('state') == state]


def sort_by_date(operations: List[Dict], reverse: bool = True) -> List[Dict]:
    """
    Сортирует список операций по дате.

    Args:
        operations: Список словарей с банковскими операциями
        reverse: Порядок сортировки (по умолчанию True - по убыванию)

    Returns:
        List[Dict]: Отсортированный список операций
    """
    def parse_date(operation: Dict) -> datetime:
        return datetime.strptime(operation['date'], '%Y-%m-%dT%H:%M:%S.%f')
    
    return sorted(operations, key=parse_date, reverse=reverse) 