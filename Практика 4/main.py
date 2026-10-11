from exceptions import MileageError
from models import Car
from services import CarService
from storage import load_json, save_csv, save_json


def show_cars(cars):
    if not cars:
        print("Список пуст.")
        return

    for car in cars:
        print(car)


def main():
    service = CarService(load_json())

    while True:
        print("\n1. Добавить автомобиль")
        print("2. Показать автомобили")
        print("3. Найти по VIN")
        print("4. Изменить пробег")
        print("5. Удалить автомобиль")
        print("6. Фильтр по максимальной цене")
        print("7. Сохранить JSON")
        print("8. Экспортировать CSV")
        print("0. Выход")

        choice = input("Выберите действие: ")

        try:
            if choice == "1":
                car = Car(
                    input("VIN: "),
                    input("Марка: "),
                    input("Модель: "),
                    int(input("Год: ")),
                    float(input("Пробег: ")),
                    float(input("Цена: "))
                )

                if car.mileage < 0:
                    raise MileageError("Пробег не может быть отрицательным.")

                service.add(car)
                print("Автомобиль добавлен.")

            elif choice == "2":
                show_cars(service.cars)

            elif choice == "3":
                car = service.find(input("VIN: "))
                print(car if car else "Автомобиль не найден.")

            elif choice == "4":
                vin = input("VIN: ")
                mileage = float(input("Новый пробег: "))

                if service.set_mileage(vin, mileage):
                    print("Пробег изменён.")
                else:
                    print("Автомобиль не найден.")

            elif choice == "5":
                if service.delete(input("VIN: ")):
                    print("Автомобиль удалён.")
                else:
                    print("Автомобиль не найден.")

            elif choice == "6":
                price = float(input("Максимальная цена: "))
                show_cars(service.filter_price(price))

            elif choice == "7":
                save_json(service.cars)
                print("Данные сохранены в cars.json.")

            elif choice == "8":
                save_csv(service.cars)
                print("Данные экспортированы в cars.csv.")

            elif choice == "0":
                save_json(service.cars)
                print("Данные сохранены. Выход.")
                break

            else:
                print("Неизвестный пункт меню.")

        except ValueError:
            print("Ошибка: введено некорректное число.")
        except MileageError as error:
            print("Ошибка:", error)


if __name__ == "__main__":
    main()
