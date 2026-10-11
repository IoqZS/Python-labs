from models import Dessert, Dish, Drink, MenuItem
from services import Notifier


class MenuFactory:
    types = {"блюдо": Dish, "напиток": Drink, "десерт": Dessert}

    @classmethod
    def create(cls, kind: str, item_id: int, name: str, price: float) -> MenuItem:
        if kind not in cls.types:
            raise ValueError("Неизвестный тип позиции")
        return cls.types[kind](item_id, name, price)


class StandardService:
    def cost(self, total: float) -> float:
        return total


class DeliveryService:
    def cost(self, total: float) -> float:
        return total + 200


class PickupService:
    def cost(self, total: float) -> float:
        return round(total * 0.9, 2)


class OrderEvents:
    """Observer: один сервис уведомляет всех подписчиков через общий интерфейс."""
    def __init__(self) -> None:
        self.observers: list[Notifier] = []

    def subscribe(self, observer: Notifier) -> None:
        self.observers.append(observer)

    def send(self, message: str) -> None:
        for observer in self.observers:
            observer.send(message)
