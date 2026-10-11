import logging
import socketserver
from domain import ProductService, Repository
from protocol import MAX_MESSAGE, encode, handle


class Handler(socketserver.StreamRequestHandler):
    def handle(self) -> None:
        self.connection.settimeout(self.server.client_timeout)
        logging.info("Подключение: %s", self.client_address)
        try:
            while line := self.rfile.readline(MAX_MESSAGE + 1):
                self.wfile.write(encode(handle(line, self.server.service)))
                self.wfile.flush()
                if len(line) > MAX_MESSAGE:
                    break
        except (OSError, TimeoutError):
            logging.exception("Соединение закрыто или истёк тайм-аут")
        finally:
            logging.info("Отключение: %s", self.client_address)


class Server(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True

    def __init__(self, address, service: ProductService, client_timeout: float = 10):
        self.service = service
        self.client_timeout = client_timeout
        super().__init__(address, Handler)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    with Server(("127.0.0.1", 9000), ProductService(Repository())) as server:
        logging.info("TCP-сервер: 127.0.0.1:9000")
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass
