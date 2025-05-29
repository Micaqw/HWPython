from typing import List, Dict
from datetime import datetime


def filter_by_state(operations: List[Dict], state: str = 'EXECUTED') -> List[Dict]:
    """
    Фильтрует список операций по статусу.
    """
    return [operation for operation in operations if operation.get('state') == state]


def sort_by_date(operations: List[Dict], reverse: bool = True) -> List[Dict]:
    """
    Сортирует список операций по дате.
    """
    def parse_date(operation: Dict) -> datetime:
        return datetime.strptime(operation['date'], '%Y-%m-%dT%H:%M:%S.%f')

    return sorted(operations, key=parse_date, reverse=reverse)
