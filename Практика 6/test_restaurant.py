import pytest
from helpers import show_report, transaction
from models import Dish, Drink, Status
from services import NotFoundError, Restaurant


def test_order_total():
    service = Restaurant()
    service.add(Dish(1, "Суп", 250))
    service.add(Drink(2, "Чай", 100))
    order = service.create_order([1, 1, 2])
    assert order.total() == 600
    assert "Суп" in show_report(service.get_item(1))
    assert "600.00" in show_report(order)


def test_status_guard():
    service = Restaurant()
    service.add(Dish(1, "Суп", 250))
    order = service.create_order([1])
    service.start_cooking(order.id)
    with pytest.raises(ValueError):
        service.start_cooking(order.id)


def test_transaction_rollback():
    collection = {1: Dish(1, "Суп", 250)}
    with pytest.raises(ValueError):
        with transaction(collection):
            collection.clear()
            raise ValueError("Ошибка")
    assert collection[1].price == 250


def test_popularity_ignores_cancelled():
    service = Restaurant()
    service.add(Dish(1, "Суп", 250))
    order = service.create_order([1, 1])
    service.change_status(order.id, Status.CANCELLED)
    assert service.popular() == []


def test_missing():
    with pytest.raises(NotFoundError):
        Restaurant().get_item(99)


def test_empty_statistics():
    assert Restaurant().statistics()["средняя цена"] == 0
