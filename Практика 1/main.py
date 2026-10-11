def fuel_usage(distance, fuel):
    return fuel / distance * 100


def average(values):
    return sum(values) / len(values)


def main():
    count = int(input("Количество поездок: "))

    if count <= 0:
        print("Количество поездок должно быть больше нуля.")
        return

    usage = []
    all_distance = 0
    all_fuel = 0

    for i in range(count):
        print(f"\nПоездка {i + 1}")
        distance = float(input("Расстояние, км: "))
        fuel = float(input("Израсходовано топлива, л: "))

        if distance <= 0 or fuel < 0:
            print("Некорректные данные.")
            return

        value = fuel_usage(distance, fuel)
        usage.append(value)

        all_distance += distance
        all_fuel += fuel

        print(f"Расход: {value:.2f} л/100 км")

    avg = average(usage)
    max_usage = max(usage)
    trip = usage.index(max_usage) + 1

    print("\nРезультаты:")
    print(f"Средний расход: {avg:.2f} л/100 км")
    print(f"Максимальный расход: поездка {trip} — {max_usage:.2f} л/100 км")
    print(f"Общий пробег: {all_distance:.2f} км")
    print(f"Общий расход топлива: {all_fuel:.2f} л")


if __name__ == "__main__":
    main()
