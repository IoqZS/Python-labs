from typing import Protocol
from models import MenuItem, Order


class Readable(Protocol):
    def get(self, entity_id: int) -> MenuItem | Order: ...
    def get_all(self) -> list: ...


class Writable(Protocol):
    def add(self, entity: MenuItem | Order) -> None: ...
    def delete(self, entity_id: int) -> None: ...


class Repository(Readable, Writable, Protocol):
    pass


class InMemoryRepository:
    def __init__(self) -> None:
        self.items: dict = {}

    def add(self, entity: MenuItem | Order) -> None:
        if entity.id in self.items:
            raise ValueError("ID уже существует")
        self.items[entity.id] = entity

    def get(self, entity_id: int) -> MenuItem | Order:
        if entity_id not in self.items:
            raise ValueError("Объект не найден")
        return self.items[entity_id]

    def get_all(self) -> list:
        return list(self.items.values())

    def delete(self, entity_id: int) -> None:
        self.get(entity_id)
        del self.items[entity_id]
