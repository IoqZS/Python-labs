import csv
import json

from models import Car


def save_json(cars, filename="cars.json"):
    data = [car.to_dict() for car in cars]

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def load_json(filename="cars.json"):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)
            return [Car.from_dict(item) for item in data]
    except FileNotFoundError:
        return []
    except (json.JSONDecodeError, KeyError):
        print("Ошибка чтения JSON. Будет использован пустой список.")
        return []


def save_csv(cars, filename="cars.csv"):
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["VIN", "brand", "model", "year", "mileage", "price"])

        for car in cars:
            writer.writerow([
                car.vin,
                car.brand,
                car.model,
                car.year,
                car.mileage,
                car.price
            ])
