from models import Dish, Drink, Status
from repository import InMemoryRepository
from services import ConsoleNotifier, Courier, MenuReport, OrderService, Pickup


def main() -> None:
    menu, orders = InMemoryRepository(), InMemoryRepository()
    service = OrderService(menu, orders, ConsoleNotifier())
    service.add_item(Dish(1, "Суп", 250))
    service.add_item(Drink(2, "Чай", 100))
    while True:
        print("\n1. Добавить  2. Меню  3. Заказ  4. Статус  5. Стоимость  6. Заказы  0. Выход")
        choice = input("Действие: ")
        try:
            if choice == "0":
                break
            if choice == "1":
                cls = {"1": Dish, "2": Drink}[input("1. Блюдо  2. Напиток: ")]
                service.add_item(cls(int(input("ID: ")), input("Название: "),
                                     float(input("Цена: "))))
            elif choice == "2":
                print(MenuReport(menu).text())
            elif choice == "3":
                print(service.create([int(n) for n in input("ID через пробел: ").split()]).report())
            elif choice == "4":
                order_id = int(input("ID заказа: "))
                print([s.value for s in Status])
                service.change_status(order_id, Status(input("Статус: ")))
            elif choice == "5":
                order_id = int(input("ID заказа: "))
                delivery = {"1": Pickup(), "2": Courier()}[input("1. Самовывоз  2. Курьер: ")]
                print("Стоимость:", service.total(order_id, delivery))
            elif choice == "6":
                for order in orders.get_all():
                    print(order.report())
            else:
                print("Неизвестная команда")
        except (ValueError, KeyError) as error:
            print("Ошибка:", error)


if __name__ == "__main__":
    main()
