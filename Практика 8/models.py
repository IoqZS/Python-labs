from dataclasses import dataclass, field
from enum import Enum


class Status(Enum):
    CREATED = "создан"
    COOKING = "готовится"
    READY = "готов"
    SERVED = "выдан"
    CANCELLED = "отменён"


@dataclass
class MenuItem:
    id: int
    name: str
    price: float

    def report(self) -> str:
        return f"{self.id}. {self.name}: {self.price:.2f} руб."


@dataclass
class Dish(MenuItem):
    weight: int = 250


@dataclass
class Drink(MenuItem):
    volume: int = 200


@dataclass
class Dessert(MenuItem):
    calories: int = 300


@dataclass
class Order:
    id: int
    items: list[MenuItem] = field(default_factory=list)
    status: Status = Status.CREATED

    def total(self) -> float:
        return sum(item.price for item in self.items)

    def report(self) -> str:
        return f"Заказ {self.id}: {self.status.value}, {self.total():.2f} руб."
