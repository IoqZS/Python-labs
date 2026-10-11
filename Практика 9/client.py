import socket
from protocol import MAX_MESSAGE, ProtocolError, decode, encode


def request(command: str, data: dict, address=("127.0.0.1", 9000), timeout=5) -> dict:
    with socket.create_connection(address, timeout=timeout) as connection:
        connection.sendall(encode({"command": command, "data": data}))
        with connection.makefile("rb") as stream:
            line = stream.readline(MAX_MESSAGE + 1)
            if not line:
                raise ProtocolError("Сервер закрыл соединение")
            return decode(line)


def main() -> None:
    commands = {"1": "list", "2": "get", "3": "add", "4": "update",
                "5": "delete", "6": "price_range"}
    while True:
        print("\n1. Список  2. Найти  3. Добавить  4. Изменить  5. Удалить  6. Цены  0. Выход")
        choice = input("Действие: ")
        if choice == "0":
            break
        try:
            command, data = commands[choice], {}
            if command in ("get", "update", "delete"):
                data["id"] = int(input("ID: "))
            if command in ("add", "update"):
                data.update(name=input("Название: "), price=float(input("Цена: ")),
                            quantity=int(input("Количество: ")))
            if command == "price_range":
                data = {"min": float(input("Минимум: ")), "max": float(input("Максимум: "))}
            print(request(command, data))
        except (OSError, ValueError, KeyError, ProtocolError) as error:
            print("Ошибка:", error)


if __name__ == "__main__":
    main()
