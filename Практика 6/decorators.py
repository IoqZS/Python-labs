from functools import wraps
from time import perf_counter


def log_call(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"[LOG] {func.__name__}")
        return func(*args, **kwargs)
    return wrapper


def timed(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = perf_counter()
        result = func(*args, **kwargs)
        print(f"[TIME] {func.__name__}: {perf_counter() - start:.6f} с")
        return result
    return wrapper


def require_status(status):
    def decorator(func):
        @wraps(func)
        def wrapper(self, order_id, *args, **kwargs):
            if self.get_order(order_id).status != status:
                raise ValueError(f"Требуется статус: {status.value}")
            return func(self, order_id, *args, **kwargs)
        return wrapper
    return decorator
