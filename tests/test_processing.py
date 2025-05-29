from typing import List, Dict
from src.processing import filter_by_state, sort_by_date


def test_filter_by_state_executed(sample_operations: List[Dict]) -> None:
    """Тест фильтрации операций со статусом EXECUTED"""
    executed_operations = filter_by_state(sample_operations, "EXECUTED")
    assert len(executed_operations) == 2
    assert all(op["state"] == "EXECUTED" for op in executed_operations)


def test_filter_by_state_canceled(sample_operations: List[Dict]) -> None:
    """Тест фильтрации операций со статусом CANCELED"""
    canceled_operations = filter_by_state(sample_operations, "CANCELED")
    assert len(canceled_operations) == 1
    assert all(op["state"] == "CANCELED" for op in canceled_operations)


def test_filter_by_state_empty_result(sample_operations: List[Dict]) -> None:
    """Тест фильтрации операций с несуществующим статусом"""
    non_existent_operations = filter_by_state(sample_operations, "NON_EXISTENT")
    assert len(non_existent_operations) == 0


def test_filter_by_state_empty_list() -> None:
    """Тест фильтрации пустого списка операций"""
    empty_operations = filter_by_state([], "EXECUTED")
    assert len(empty_operations) == 0


def test_sort_by_date_descending(sample_operations: List[Dict]) -> None:
    """Тест сортировки операций по дате по убыванию"""
    sorted_operations = sort_by_date(sample_operations, reverse=True)
    dates = [op["date"] for op in sorted_operations]
    assert dates == sorted(dates, reverse=True)


def test_sort_by_date_ascending(sample_operations: List[Dict]) -> None:
    """Тест сортировки операций по дате по возрастанию"""
    sorted_operations = sort_by_date(sample_operations, reverse=False)
    dates = [op["date"] for op in sorted_operations]
    assert dates == sorted(dates)


def test_sort_by_date_empty_list() -> None:
    """Тест сортировки пустого списка операций"""
    empty_operations = sort_by_date([], reverse=True)
    assert empty_operations == []
