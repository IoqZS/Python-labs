from typing import Protocol
from models import MenuItem, Order, Status
from repository import Readable, Repository


class Notifier(Protocol):
    def send(self, message: str) -> None: ...


class Delivery(Protocol):
    def cost(self, total: float) -> float: ...


class Pickup:
    def cost(self, total: float) -> float:
        return total


class Courier:
    def cost(self, total: float) -> float:
        return total + 200


class ConsoleNotifier:
    def send(self, message: str) -> None:
        print("Уведомление:", message)


class MessageNotifier:
    def __init__(self) -> None:
        self.messages: list[str] = []

    def send(self, message: str) -> None:
        self.messages.append(message)


class MenuReport:
    """Для отчёта нужен только интерфейс чтения (ISP)."""
    def __init__(self, repository: Readable) -> None:
        self.repository = repository

    def text(self) -> str:
        return "\n".join(item.report() for item in self.repository.get_all())


class OrderService:
    def __init__(self, menu: Repository, orders: Repository, notifier: Notifier) -> None:
        self.menu = menu
        self.orders = orders
        self.notifier = notifier
        self.next_id = 1

    def add_item(self, item: MenuItem) -> None:
        if item.id <= 0 or not item.name.strip() or item.price <= 0:
            raise ValueError("Нужны название, положительные ID и цена")
        self.menu.add(item)

    def create(self, ids: list[int]) -> Order:
        if not ids:
            raise ValueError("Заказ пуст")
        order = Order(self.next_id, [self.menu.get(i) for i in ids])
        self.orders.add(order)
        self.next_id += 1
        self.notifier.send(f"Заказ {order.id} создан")
        return order

    def change_status(self, order_id: int, status: Status) -> None:
        order = self.orders.get(order_id)
        transitions = {Status.CREATED: (Status.COOKING, Status.CANCELLED),
                       Status.COOKING: (Status.READY, Status.CANCELLED),
                       Status.READY: (Status.SERVED,)}
        if status not in transitions.get(order.status, ()):
            raise ValueError("Недопустимый переход")
        order.status = status
        self.notifier.send(f"Заказ {order.id}: {status.value}")

    def total(self, order_id: int, delivery: Delivery) -> float:
        return delivery.cost(self.orders.get(order_id).total())
