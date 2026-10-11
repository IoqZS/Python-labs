from helpers import inspect_object, show_report, transaction
from models import Dish, Drink, Status
from services import NotFoundError, Restaurant


def main() -> None:
    restaurant = Restaurant()
    restaurant.add(Dish(1, "Суп", 250))
    restaurant.add(Drink(2, "Чай", 100))
    while True:
        print("\n1. Добавить  2. Удалить  3. Найти  4. Меню и заказы")
        print("5. Статус  6. Создать заказ  7. Статистика  8. Интроспекция")
        print("9. Декораторы  10. Контекстный менеджер  11. Популярные блюда  0. Выход")
        choice = input("Действие: ")
        try:
            if choice == "0":
                break
            if choice == "1":
                cls = {"1": Dish, "2": Drink}[input("1. Блюдо  2. Напиток: ")]
                restaurant.add(cls(int(input("ID: ")), input("Название: "),
                                   float(input("Цена: "))))
            elif choice == "2":
                restaurant.remove(int(input("ID позиции: ")))
            elif choice in ("3", "8"):
                item = restaurant.get_item(int(input("ID позиции: ")))
                print(show_report(item) if choice == "3" else inspect_object(item))
            elif choice == "4":
                for obj in [*restaurant.menu.values(), *restaurant.orders.values()]:
                    print(show_report(obj))
            elif choice == "5":
                order_id = int(input("ID заказа: "))
                statuses = list(Status)
                print([(i + 1, s.value) for i, s in enumerate(statuses)])
                number = int(input("Номер статуса: "))
                if not 1 <= number <= len(statuses):
                    raise ValueError("Нет такого статуса")
                restaurant.change_status(order_id, statuses[number - 1])
            elif choice == "6":
                ids = [int(n) for n in input("ID позиций через пробел: ").split()]
                print(show_report(restaurant.create_order(ids)))
            elif choice == "7":
                print(restaurant.statistics())
            elif choice == "9":
                order = restaurant.create_order([1])
                restaurant.start_cooking(order.id)
                print(show_report(order), restaurant.statistics())
            elif choice == "10":
                try:
                    with transaction(restaurant.menu):
                        restaurant.menu.clear()
                        raise ValueError("Учебная ошибка — меню будет восстановлено")
                except ValueError as error:
                    print(error, "Позиции:", len(restaurant.menu))
            elif choice == "11":
                print(restaurant.popular())
            else:
                print("Неизвестная команда")
        except (ValueError, KeyError, NotFoundError) as error:
            print("Ошибка:", error)


if __name__ == "__main__":
    main()
