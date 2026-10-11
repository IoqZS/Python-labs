import json
import logging
from domain import NotFoundError, ProductService, ValidationError

MAX_MESSAGE = 65536


class ProtocolError(Exception):
    pass


def encode(message: dict) -> bytes:
    return (json.dumps(message, ensure_ascii=False, allow_nan=False) + "\n").encode("utf-8")


def decode(line: bytes) -> dict:
    if not line.endswith(b"\n") or len(line) > MAX_MESSAGE:
        raise ProtocolError("Сообщение слишком длинное или нет символа новой строки")
    try:
        message = json.loads(line)
    except (ValueError, UnicodeError) as error:
        raise ProtocolError("Некорректный JSON") from error
    if not isinstance(message, dict):
        raise ProtocolError("Нужен JSON-объект")
    return message


def handle(line: bytes, service: ProductService) -> dict:
    try:
        request = decode(line)
        command = request.get("command")
        if not isinstance(command, str):
            raise ProtocolError("Нет поля command")
        logging.info("Команда: %s", command)
        result = service.execute(command, request.get("data", {}))
        logging.info("Команда выполнена: %s", command)
        return {"status": "ok", "data": result, "error": None}
    except (ProtocolError, ValidationError, NotFoundError) as error:
        logging.warning("Ошибка запроса: %s", error)
        return {"status": "error", "data": None, "error": str(error)}
