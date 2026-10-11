class Car:
    def __init__(self, brand, model, year, mileage, price):
        self.brand = brand
        self.model = model
        self.year = year
        self.mileage = mileage
        self.price = price

    def get_type(self):
        return "Автомобиль"

    def __str__(self):
        return (
            f"{self.brand} {self.model}, {self.year}, "
            f"{self.mileage} км, {self.price:.2f}, {self.get_type()}"
        )


class PetrolCar(Car):
    def get_type(self):
        return "Бензиновый"


class ElectricCar(Car):
    def get_type(self):
        return "Электромобиль"


def map_cars(cars, func):
    return list(map(func, cars))


def filter_cars(cars, condition):
    return list(filter(condition, cars))


def cars_by_brand(cars, brand):
    for car in cars:
        if car.brand.lower() == brand.lower():
            yield car


def main():
    cars = [
        PetrolCar("Toyota", "Camry", 2020, 50000, 2500000),
        ElectricCar("Tesla", "Model 3", 2022, 30000, 4000000),
        PetrolCar("BMW", "X5", 2019, 80000, 3500000)
    ]

    while True:
        print("\n1. Показать все автомобили")
        print("2. Фильтр по цене")
        print("3. Показать модели")
        print("4. Сортировать по пробегу")
        print("5. Самый дорогой автомобиль")
        print("6. Автомобили по марке")
        print("7. Проверить год")
        print("8. Показать работу генератора")
        print("0. Выход")

        choice = input("Выберите действие: ")

        try:
            if choice == "1":
                texts = [str(car) for car in cars]

                for text in texts:
                    print(text)

            elif choice == "2":
                price = float(input("Максимальная цена: "))
                result = filter_cars(cars, lambda car: car.price <= price)

                for car in result:
                    print(car)

            elif choice == "3":
                models = map_cars(cars, lambda car: car.model)
                print("Модели:", models)

            elif choice == "4":
                result = sorted(cars, key=lambda car: car.mileage)
                for car in result:
                    print(car)

            elif choice == "5":
                car = max(cars, key=lambda car: car.price)
                print(car)

            elif choice == "6":
                brand = input("Марка: ")
                result = cars_by_brand(cars, brand)
                first = next(result, None)

                if first is None:
                    print("Автомобили не найдены.")
                else:
                    print(first)

                    for car in result:
                        print(car)

            elif choice == "7":
                year = int(input("Год: "))
                old = any(car.year < year for car in cars)
                print("Есть автомобили старше:", old)

            elif choice == "8":
                values = [x * x for x in range(5)]
                numbers = (x * x for x in range(5))

                print("Обычный список:", values)
                print("Первое значение генератора:", next(numbers))

            elif choice == "0":
                break

            else:
                print("Неизвестная команда.")

        except ValueError:
            print("Ошибка: необходимо ввести число.")


if __name__ == "__main__":
    main()
