from concurrent.futures import ThreadPoolExecutor
import socket
from threading import Thread
import pytest
from client import request
from domain import NotFoundError, ProductService, Repository, ValidationError
from protocol import decode, encode, handle
from server import Server

DATA = {"name": "Книга", "price": 300, "quantity": 5}


def test_repository_add():
    repo = Repository()
    product = repo.add(DATA)
    assert repo.get(product.id).name == "Книга"


def test_repository_delete():
    repo = Repository()
    product = repo.add(DATA)
    repo.delete(product.id)
    with pytest.raises(NotFoundError):
        repo.get(product.id)


def test_service_range():
    service = ProductService(Repository())
    service.execute("add", DATA)
    assert len(service.execute("price_range", {"min": 300, "max": 300})) == 1
    assert service.execute("price_range", {"min": 400, "max": 500}) == []


def test_service_invalid():
    service = ProductService(Repository())
    with pytest.raises(ValidationError):
        service.execute("add", {**DATA, "price": -10})


def test_protocol():
    message = {"command": "add", "data": DATA}
    assert decode(encode(message)) == message
    service = ProductService(Repository())
    assert handle(b"bad\n", service)["status"] == "error"
    assert handle(encode({"command": "unknown"}), service)["status"] == "error"


def test_three_clients():
    service = ProductService(Repository())
    with Server(("127.0.0.1", 0), service) as server:
        thread = Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            with ThreadPoolExecutor(max_workers=3) as pool:
                results = list(pool.map(lambda _: request("add", DATA, server.server_address), range(3)))
            assert all(r["status"] == "ok" for r in results)
            assert len({r["data"]["id"] for r in results}) == 3
            assert len(request("list", {}, server.server_address)["data"]) == 3
        finally:
            server.shutdown()
            thread.join()


def test_server_idle_timeout():
    with Server(("127.0.0.1", 0), ProductService(Repository()), client_timeout=0.1) as server:
        thread = Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            with socket.create_connection(server.server_address, timeout=2) as client:
                assert client.recv(1) == b""
        finally:
            server.shutdown()
            thread.join()


def test_client_timeout():
    with socket.socket() as listener:
        listener.bind(("127.0.0.1", 0))
        listener.listen()
        with pytest.raises(TimeoutError):
            request("list", {}, listener.getsockname(), timeout=0.1)
