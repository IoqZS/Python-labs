"""Лабораторная №7, вариант 6 (ресторан): версия ДО рефакторинга.

Программа намеренно содержит пять архитектурных проблем SOLID.
Это рабочая демонстрация исходного состояния, а НЕ образец хорошей архитектуры.
Исправленный вариант находится в models.py, repository.py и services.py.

SRP — класс RestaurantBefore выполняет сразу несколько обязанностей.
OCP — в RestaurantBefore.create выбор доставки реализован через if/elif.
LSP — PickupBefore нарушает контракт родительского DeliveryMethodBefore.
ISP — RestaurantGatewayBefore слишком велик для OrderReportBefore.
DIP — RestaurantBefore самостоятельно создаёт ConsoleNotifierBefore.
"""

from typing import Protocol


# ПРОБЛЕМА 4 — ISP: один «толстый» интерфейс для всех видов работы.
# Отчёту нужен лишь get_orders(), однако формально он зависит и от операций
# добавления, изменения и удаления. После рефакторинга — Readable и Writable.
class RestaurantGatewayBefore(Protocol):
    def add_dish(self, name: str, price: float) -> None: ...

    def create(self, prices: list[float], delivery: str) -> float: ...

    def change_status(self, order_id: int, status: str) -> None: ...

    def get_orders(self) -> list[dict]: ...

    def remove_order(self, order_id: int) -> None: ...


class OrderReportBefore:
    def __init__(self, restaurant: RestaurantGatewayBefore) -> None:
        self.restaurant = restaurant

    def text(self) -> str:
        # Нужен только один метод из пяти (нарушение ISP).
        return "\n".join(
            f"Заказ {order['id']}: {order['status']}, {order['total']:.2f} руб."
            for order in self.restaurant.get_orders()
        )


# ПРОБЛЕМА 3 — LSP: базовый класс обещает доставку по адресу.
# Однако самовывоз не может выполнить этот контракт и выбрасывает исключение.
class DeliveryMethodBefore:
    def cost(self, total: float) -> float:
        return total + 200

    def deliver_to_address(self, address: str) -> str:
        return f"Доставлено по адресу: {address}"


class CourierBefore(DeliveryMethodBefore):
    pass


class PickupBefore(DeliveryMethodBefore):
    def cost(self, total: float) -> float:
        return total

    def deliver_to_address(self, address: str) -> str:
        raise NotImplementedError("Самовывоз нельзя доставить по адресу")


def request_address_delivery(method: DeliveryMethodBefore, address: str) -> str:
    """Ожидает, что любая реализация DeliveryMethodBefore выполнит контракт."""
    return method.deliver_to_address(address)


class ConsoleNotifierBefore:
    def send(self, message: str) -> None:
        print("Уведомление:", message)


# ПРОБЛЕМА 1 — SRP: один класс управляет меню, заказами, расчётами,
# статусами и выводом. У него несколько независимых причин для изменения.
class RestaurantBefore:
    def __init__(self) -> None:
        self.menu: dict[str, float] = {}
        self.orders: list[dict] = []
        self.next_id = 1

        # ПРОБЛЕМА 5 — DIP: зависимость создаётся внутри бизнес-класса.
        # Нельзя передать тестовый уведомитель без изменения RestaurantBefore.
        self.notifier = ConsoleNotifierBefore()

    def add_dish(self, name: str, price: float) -> None:
        if not name.strip() or price <= 0:
            raise ValueError("У блюда должны быть название и положительная цена")
        self.menu[name] = price
        print("Блюдо добавлено:", name)

    def create(self, prices: list[float], delivery: str) -> float:
        if not prices or any(price <= 0 for price in prices):
            raise ValueError("Заказ должен содержать позиции с положительной ценой")
        total = sum(prices)

        # ПРОБЛЕМА 2 — OCP: для каждого нового типа доставки приходится
        # изменять этот метод. После рефакторинга используются Pickup/Courier
        # и общий интерфейс Delivery с методом cost().
        if delivery == "courier":
            total += 200
        elif delivery == "pickup":
            pass
        else:
            raise ValueError("Неизвестный способ доставки")

        self.orders.append({"id": self.next_id, "status": "создан", "total": total})
        print(f"Заказ {self.next_id} создан. Стоимость: {total:.2f} руб.")
        self.notifier.send(f"Заказ {self.next_id} создан")
        self.next_id += 1
        return total

    def change_status(self, order_id: int, status: str) -> None:
        for order in self.orders:
            if order["id"] == order_id:
                order["status"] = status
                print(f"Заказ {order_id}: {status}")
                self.notifier.send(f"Заказ {order_id}: {status}")
                return
        raise ValueError("Заказ не найден")

    def get_orders(self) -> list[dict]:
        return list(self.orders)

    def remove_order(self, order_id: int) -> None:
        for order in self.orders:
            if order["id"] == order_id:
                self.orders.remove(order)
                print(f"Заказ {order_id} удалён")
                return
        raise ValueError("Заказ не найден")


if __name__ == "__main__":
    print("=== Ресторан: архитектура ДО рефакторинга ===")
    restaurant = RestaurantBefore()
    restaurant.add_dish("Суп", 250)
    restaurant.add_dish("Чай", 100)
    restaurant.create([250, 100], "courier")
    restaurant.change_status(1, "готовится")
    print("\nОтчёт о заказах:")
    print(OrderReportBefore(restaurant).text())

    print("\nКорректная доставка:")
    print(request_address_delivery(CourierBefore(), "ул. Центральная, 1"))
    print("\nНарушение LSP (самовывоз вместо доставки):")
    try:
        print(request_address_delivery(PickupBefore(), "ул. Центральная, 1"))
    except NotImplementedError as error:
        print("Ошибка подстановки:", error)
