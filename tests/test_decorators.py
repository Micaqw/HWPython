import pytest
import logging
import os
from typing import Any
import io
from src.decorators import log


@pytest.fixture
def captured_logs():
    """Фикстура для перехвата логов."""
    log_capture = io.StringIO()
    handler = logging.StreamHandler(log_capture)
    root_logger = logging.getLogger()
    root_logger.addHandler(handler)
    root_logger.setLevel(logging.INFO)
    
    yield log_capture
    
    root_logger.removeHandler(handler)
    handler.close()


@pytest.fixture
def reset_logging():
    """Фикстура для сброса настроек логирования."""
    yield
    logging.shutdown()
    root_logger = logging.getLogger()
    root_logger.handlers.clear()
    logging.basicConfig(handlers=[], level=logging.INFO)


def test_logsuccess_console(captured_logs: Any) -> None:
    """Тест успешного логирования в консоль."""
    @log()
    def add(x: int, y: int) -> int:
        return x + y

    assert add(2, 3) == 5
    output = captured_logs.getvalue()
    assert "Функция 'add' начата" in output
    assert "Функция 'add' окончена, результат: 5" in output


def test_logerror_console(captured_logs: Any) -> None:
    """Тест логирования ошибки в консоль."""
    @log()
    def divide(x: float, y: float) -> float:
        return x / y

    with pytest.raises(ZeroDivisionError):
        divide(5, 0)

    output = captured_logs.getvalue()
    assert "Функция 'divide' начата" in output
    assert "Ошибка в функции 'divide' Ошибка: ZeroDivisionError" in output
    assert "Функция 'divide' окончена" not in output


def test_logpreserves_function_name() -> None:
    """Тест сохранения оригинального имени функции."""
    @log()
    def greet() -> None:
        pass

    assert greet.__name__ == "greet"


def test_log_to_file() -> None:
    """Тест логирования в файл."""
    log_file = "test_decorator.log"
    
    try:
        @log(filename=log_file)
        def multiply(x: int, y: int) -> int:
            return x * y
        
        result = multiply(4, 5)
        assert result == 20
        
        # Проверяем содержимое лог-файла
        assert os.path.exists(log_file), "Log file should exist"
        with open(log_file, encoding='utf-8') as f:
            log_content = f.read()
            assert "Функция 'multiply' начата" in log_content
            assert "Функция 'multiply' окончена, результат: 20" in log_content
    finally:
        # Очищаем после теста
        if os.path.exists(log_file):
            os.remove(log_file)
        # Сбрасываем настройки логирования
        logging.shutdown()
        root_logger = logging.getLogger()
        root_logger.handlers.clear()
        logging.basicConfig(handlers=[], level=logging.INFO)