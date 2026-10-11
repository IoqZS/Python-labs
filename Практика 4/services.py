from exceptions import MileageError


class CarService:
    def __init__(self, cars=None):
        self.cars = cars if cars is not None else []

    def add(self, car):
        self.cars.append(car)

    def find(self, vin):
        for car in self.cars:
            if car.vin == vin:
                return car
        return None

    def set_mileage(self, vin, mileage):
        if mileage < 0:
            raise MileageError("Пробег не может быть отрицательным.")

        car = self.find(vin)

        if car is None:
            return False

        car.mileage = mileage
        return True

    def delete(self, vin):
        car = self.find(vin)

        if car is None:
            return False

        self.cars.remove(car)
        return True

    def filter_price(self, max_price):
        return [car for car in self.cars if car.price <= max_price]
