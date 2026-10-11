class Car:
    def __init__(self, vin, brand, model, year, mileage, price):
        self.vin = vin
        self.brand = brand
        self.model = model
        self.year = year
        self.mileage = mileage
        self.price = price

    def to_dict(self):
        return {
            "vin": self.vin,
            "brand": self.brand,
            "model": self.model,
            "year": self.year,
            "mileage": self.mileage,
            "price": self.price
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["vin"],
            data["brand"],
            data["model"],
            data["year"],
            data["mileage"],
            data["price"]
        )

    def __str__(self):
        return (
            f"{self.vin}: {self.brand} {self.model}, {self.year}, "
            f"{self.mileage} км, {self.price:.2f}"
        )
