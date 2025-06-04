import logging
import functools
from typing import Any, Callable, Optional, TypeVar


T = TypeVar('T')


def log(filename: Optional[str] = None) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """Декоратор для логирования вызовов функций.

    Args:
        filename: Путь к файлу для записи логов. Если None, логи выводятся в консоль.

    Returns:
        Декорированная функция с добавленным логированием.
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            func_name = func.__name__
            logging.basicConfig(
                filename=filename,
                level=logging.INFO,
                format='%(asctime)s - %(levelname)s - %(message)s'
            )
            logging.info(f"Функция '{func_name}' начата")

            try:
                result = func(*args, **kwargs)
                logging.info(f"Функция '{func_name}' окончена, результат: {result}")
                return result
            except Exception as e:
                logging.basicConfig(
                    filename=filename,
                    level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s - %(message)s'
                )
                logging.error(
                    f"Ошибка в функции '{func_name}' "
                    f"Ошибка: {type(e).__name__}. "
                    f"Вводные данные: {args}, {kwargs}"
                )
                raise
        return wrapper
    return decorator 