from collections import Counter
from decorators import log_call, require_status, timed
from models import Dish, MenuItem, Order, Status


class NotFoundError(Exception):
    pass


class Restaurant:
    def __init__(self) -> None:
        self.menu: dict[int, MenuItem] = {}
        self.orders: dict[int, Order] = {}
        self.next_order = 1

    @log_call
    def add(self, item: MenuItem) -> None:
        if not item.name.strip() or item.price <= 0 or item.id <= 0:
            raise ValueError("Нужны название, положительные цена и ID")
        if item.id in self.menu:
            raise ValueError("Такой ID уже есть")
        self.menu[item.id] = item

    def get_item(self, item_id: int) -> MenuItem:
        if item_id not in self.menu:
            raise NotFoundError("Позиция меню не найдена")
        return self.menu[item_id]

    def remove(self, item_id: int) -> None:
        self.get_item(item_id)
        del self.menu[item_id]

    def create_order(self, item_ids: list[int]) -> Order:
        if not item_ids:
            raise ValueError("Заказ не должен быть пустым")
        order = Order(self.next_order, [self.get_item(i) for i in item_ids])
        self.orders[order.id] = order
        self.next_order += 1
        return order

    def get_order(self, order_id: int) -> Order:
        if order_id not in self.orders:
            raise NotFoundError("Заказ не найден")
        return self.orders[order_id]

    def change_status(self, order_id: int, status: Status) -> None:
        order = self.get_order(order_id)
        transitions = {
            Status.CREATED: (Status.COOKING, Status.CANCELLED),
            Status.COOKING: (Status.READY, Status.CANCELLED),
            Status.READY: (Status.SERVED,),
        }
        if status not in transitions.get(order.status, ()):
            raise ValueError("Недопустимое изменение статуса")
        order.status = status

    @require_status(Status.CREATED)
    def start_cooking(self, order_id: int) -> None:
        self.change_status(order_id, Status.COOKING)

    def popular(self) -> list[tuple[str, int]]:
        counts = Counter(item.name for order in self.orders.values()
                        if order.status != Status.CANCELLED
                        for item in order.items if isinstance(item, Dish))
        return counts.most_common()

    @timed
    def statistics(self) -> dict:
        prices = [item.price for item in self.menu.values()]
        return {"позиций": len(prices), "заказов": len(self.orders),
                "средняя цена": sum(prices) / len(prices) if prices else 0,
                "минимум": min(prices, default=0), "максимум": max(prices, default=0)}
