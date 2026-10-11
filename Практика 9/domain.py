from dataclasses import asdict, dataclass, replace
from math import isfinite
from threading import RLock


class ValidationError(Exception):
    pass


class NotFoundError(Exception):
    pass


@dataclass
class Product:
    id: int
    name: str
    price: float
    quantity: int


class Repository:
    def __init__(self) -> None:
        self.items: dict[int, Product] = {}
        self.next_id = 1
        self.lock = RLock()

    def get(self, item_id: int) -> Product:
        with self.lock:
            if item_id not in self.items:
                raise NotFoundError("Товар не найден")
            return replace(self.items[item_id])

    def get_all(self) -> list[Product]:
        with self.lock:
            return [replace(item) for item in self.items.values()]

    def add(self, data: dict) -> Product:
        with self.lock:
            product = Product(self.next_id, **data)
            self.items[product.id] = product
            self.next_id += 1
            return replace(product)

    def update(self, item_id: int, data: dict) -> Product:
        with self.lock:
            self.get(item_id)
            self.items[item_id] = Product(item_id, **data)
            return self.get(item_id)

    def delete(self, item_id: int) -> None:
        with self.lock:
            self.get(item_id)
            del self.items[item_id]


class ProductService:
    def __init__(self, repository: Repository) -> None:
        self.repository = repository

    def validate(self, data: dict) -> dict:
        if not isinstance(data, dict) or set(data) != {"name", "price", "quantity"}:
            raise ValidationError("Нужны поля name, price, quantity")
        if not isinstance(data["name"], str) or not data["name"].strip():
            raise ValidationError("Название не должно быть пустым")
        price, quantity = data["price"], data["quantity"]
        if type(price) not in (int, float) or not isfinite(price) or price <= 0:
            raise ValidationError("Цена должна быть положительным числом")
        if type(quantity) is not int or quantity < 0:
            raise ValidationError("Количество должно быть целым и неотрицательным")
        return {**data, "name": data["name"].strip()}

    def execute(self, command: str, data: dict):
        if not isinstance(data, dict):
            raise ValidationError("data должен быть объектом")
        if command == "list":
            return [asdict(p) for p in self.repository.get_all()]
        if command == "add":
            return asdict(self.repository.add(self.validate(data)))
        if command == "price_range":
            low, high = data.get("min"), data.get("max")
            if any(type(n) not in (int, float) or not isfinite(n) for n in (low, high)):
                raise ValidationError("Нужны числовые min и max")
            if low < 0 or high < low:
                raise ValidationError("Неверный диапазон цены")
            return [asdict(p) for p in self.repository.get_all() if low <= p.price <= high]
        if command not in ("get", "update", "delete"):
            raise ValidationError("Неизвестная команда")
        item_id = data.get("id")
        if type(item_id) is not int or item_id <= 0:
            raise ValidationError("Нужен положительный целый id")
        if command == "get":
            return asdict(self.repository.get(item_id))
        if command == "update":
            fields = {k: v for k, v in data.items() if k != "id"}
            return asdict(self.repository.update(item_id, self.validate(fields)))
        self.repository.delete(item_id)
        return {"message": "Товар удалён"}
