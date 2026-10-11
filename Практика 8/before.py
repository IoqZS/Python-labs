"""До паттернов: создание, расчёт и уведомления через условия."""
def process(kind, price, mode):
    if kind == "блюдо":
        item = {"name": "Суп", "price": price}
    elif kind == "напиток":
        item = {"name": "Чай", "price": price}
    elif kind == "десерт":
        item = {"name": "Торт", "price": price}
    else:
        raise ValueError("Неизвестный тип")
    if mode == "доставка":
        total = item["price"] + 200
    elif mode == "самовывоз":
        total = round(item["price"] * 0.9, 2)
    elif mode == "зал":
        total = item["price"]
    else:
        raise ValueError("Неизвестный режим")
    print("Клиенту: заказ создан")
    print("Журнал: заказ создан")
    return total


if __name__ == "__main__":
    print(process("блюдо", 250, "доставка"))
