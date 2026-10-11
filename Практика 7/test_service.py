import pytest
from models import Dish, Drink, Status
from repository import InMemoryRepository
from services import Courier, MessageNotifier, OrderService, Pickup


@pytest.fixture
def service():
    service = OrderService(InMemoryRepository(), InMemoryRepository(), MessageNotifier())
    service.add_item(Dish(1, "Суп", 250))
    service.add_item(Drink(2, "Чай", 100))
    return service


def test_total(service):
    order = service.create([1, 2])
    assert service.total(order.id, Pickup()) == 350
    assert service.total(order.id, Courier()) == 550


def test_notification(service):
    service.create([1])
    assert service.notifier.messages == ["Заказ 1 создан"]


def test_missing_item(service):
    with pytest.raises(ValueError):
        service.create([99])
    assert service.orders.get_all() == []


def test_invalid_price(service):
    with pytest.raises(ValueError):
        service.add_item(Dish(3, "Суп", -1))


def test_status(service):
    order = service.create([1])
    service.change_status(order.id, Status.COOKING)
    assert order.status == Status.COOKING
    with pytest.raises(ValueError):
        service.change_status(order.id, Status.CREATED)


def test_lsp(service):
    class FreeDelivery:
        def cost(self, total):
            return total
    order = service.create([2])
    assert service.total(order.id, FreeDelivery()) == 100
