from models import Status
from patterns import DeliveryService, MenuFactory, OrderEvents, PickupService, StandardService
from repository import InMemoryRepository
from services import ConsoleNotifier, MenuReport, MessageNotifier, OrderService


def main() -> None:
    menu, orders = InMemoryRepository(), InMemoryRepository()
    events, journal = OrderEvents(), MessageNotifier()
    events.subscribe(ConsoleNotifier())
    events.subscribe(journal)
    service = OrderService(menu, orders, events)
    service.add_item(MenuFactory.create("блюдо", 1, "Суп", 250))
    service.add_item(MenuFactory.create("напиток", 2, "Чай", 100))
    service.add_item(MenuFactory.create("десерт", 3, "Торт", 200))
    while True:
        print("\n1. Добавить  2. Меню  3. Заказ  4. Статус  5. Расчёт  6. Журнал  0. Выход")
        choice = input("Действие: ")
        try:
            if choice == "0":
                break
            if choice == "1":
                kind = input("Тип (блюдо/напиток/десерт): ")
                service.add_item(MenuFactory.create(kind, int(input("ID: ")),
                                                    input("Название: "), float(input("Цена: "))))
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
                strategies = {"1": StandardService(), "2": DeliveryService(), "3": PickupService()}
                strategy = strategies[input("1. В зале  2. Доставка  3. Самовывоз: ")]
                print("Стоимость:", service.total(order_id, strategy))
            elif choice == "6":
                print("\n".join(journal.messages))
            else:
                print("Неизвестная команда")
        except (ValueError, KeyError) as error:
            print("Ошибка:", error)


if __name__ == "__main__":
    main()
