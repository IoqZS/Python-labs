def find_brand(cars, brand):
    result = []

    for car in cars:
        if car["brand"].lower() == brand.lower():
            result.append(car)

    return result


def filter_mileage(cars, max_mileage):
    result = []

    for car in cars:
        if car["mileage"] <= max_mileage:
            result.append(car)

    return result


def average_price(cars):
    total = 0

    for car in cars:
        total += car["price"]

    return total / len(cars)


def show_cars(cars):
    for (i, car) in enumerate(cars, start=1):
        print(
            f'{i}) '
            f'{car["brand"]} {car["model"]}, '
            f'{car["year"]}, пробег {car["mileage"]} км, '
            f'цена {car["price"]:.2f}'
        )


def main():
    count = int(input("Количество автомобилей: "))

    if count <= 0:
        print("Количество должно быть больше нуля.")
        return

    cars = []

    for i in range(count):
        print(f"\nАвтомобиль {i + 1}")
        car = {
            "brand": input("Марка: "),
            "model": input("Модель: "),
            "year": int(input("Год выпуска: ")),
            "mileage": float(input("Пробег: ")),
            "price": float(input("Цена: "))
        }

        if car["mileage"] < 0 or car["price"] < 0:
            print("Пробег и цена не могут быть отрицательными.")
            return

        cars.append(car)

    print("\nВсе автомобили:")
    show_cars(cars)

    brand = input("\nМарка для поиска: ")
    found = find_brand(cars, brand)
    print("Результат поиска:")
    show_cars(found) if found else print("Ничего не найдено.")

    max_mileage = float(input("\nМаксимальный пробег для фильтрации: "))
    filtered = filter_mileage(cars, max_mileage)
    print("Результат фильтрации:")
    show_cars(filtered) if filtered else print("Ничего не найдено.")

    expensive = max(cars, key=lambda car: car["price"])
    cheap = min(cars, key=lambda car: car["price"])

    print("\nСтатистика:")
    print(f"Средняя цена: {average_price(cars):.2f}")
    print(f"Максимальная цена: {expensive['price']:.2f}")
    print(f"Минимальная цена: {cheap['price']:.2f}")

    brands = set(car["brand"] for car in cars)
    print("Уникальные марки:", ", ".join(brands))

    sorted_cars = sorted(cars, key=lambda car: car["price"])
    print("\nСортировка по цене:")
    show_cars(sorted_cars)


if __name__ == "__main__":
    main()
