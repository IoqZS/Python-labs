from contextlib import contextmanager
from copy import deepcopy
from inspect import signature
from typing import Iterator, Protocol


class Reportable(Protocol):
    def report(self) -> str:
        ...


def show_report(obj: Reportable) -> str:
    return obj.report()


@contextmanager
def transaction(collection: dict) -> Iterator[None]:
    """Если операция завершилась ошибкой, восстановить коллекцию."""
    backup = deepcopy(collection)
    try:
        # Здесь выполняется код внутри with.
        yield
    except Exception:
        # При ошибке возвращаем сохранённые данные.
        collection.clear()
        collection.update(backup)
        raise


def inspect_object(obj: Reportable) -> dict:
    attributes = []
    for name in dir(obj):
        if not name.startswith("_"):
            attributes.append(name)

    return {
        "тип": type(obj).__name__,
        "атрибуты": attributes,
        "есть report": hasattr(obj, "report"),
        "id": getattr(obj, "id", None),
        "сигнатура report": str(signature(obj.report)),
    }
