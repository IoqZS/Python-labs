import pytest
from models import Dessert, Dish, Drink, Status
from patterns import DeliveryService, MenuFactory, OrderEvents, PickupService, StandardService
from repository import InMemoryRepository
from services import MessageNotifier, OrderService


@pytest.mark.parametrize("kind, cls", [("блюдо", Dish), ("напиток", Drink), ("десерт", Dessert)])
def test_factory(kind, cls):
    assert isinstance(MenuFactory.create(kind, 1, "Позиция", 100), cls)


def test_invalid_factory():
    with pytest.raises(ValueError):
        MenuFactory.create("неизвестно", 1, "Позиция", 100)


@pytest.mark.parametrize("strategy, total", [(StandardService(), 100), (DeliveryService(), 300),
                                            (PickupService(), 90)])
def test_strategy(strategy, total):
    assert strategy.cost(100) == total


def test_observers():
    events = OrderEvents()
    first, second = MessageNotifier(), MessageNotifier()
    events.subscribe(first)
    events.subscribe(second)
    service = OrderService(InMemoryRepository(), InMemoryRepository(), events)
    service.add_item(MenuFactory.create("блюдо", 1, "Суп", 250))
    order = service.create([1])
    service.change_status(order.id, Status.COOKING)
    assert first.messages == second.messages == ["Заказ 1 создан", "Заказ 1: готовится"]


def test_repository_delete():
    repo = InMemoryRepository()
    repo.add(Dish(1, "Суп", 250))
    repo.delete(1)
    assert repo.get_all() == []


def test_failed_order():
    service = OrderService(InMemoryRepository(), InMemoryRepository(), MessageNotifier())
    with pytest.raises(ValueError):
        service.create([99])
    assert service.orders.get_all() == []
