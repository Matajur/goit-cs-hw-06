"""Basic WEB application with HTML and Socket servers"""

import asyncio
import logging
import json
import mimetypes
import pathlib
import urllib.parse
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from multiprocessing import Process

import websockets

from src.connection import (
    provide_db_collection,
    HTTP_SERVER_HOST,
    HTTP_SERVER_PORT,
    SOCKET_SERVER_HOST,
    SOCKET_SERVER_PORT,
)

logging.basicConfig(level=logging.INFO)


class HttpHandler(BaseHTTPRequestHandler):
    """
    Class that handles all requests to HTTP server
    """

    async def send_message(self, message: str):
        """
        Asynchronous function methon that sends messages from HTTP to Socket server

        :param message: The message to send
        """
        ws_resource_url = f"ws://{SOCKET_SERVER_HOST}:{SOCKET_SERVER_PORT}"
        async with websockets.connect(ws_resource_url) as websocket:
            await websocket.send(message)

    def do_POST(self):
        """
        Method that handles POST requests to the HTTP server
        """
        pr_url = urllib.parse.urlparse(self.path)
        if pr_url.path == "/message":
            data = self.rfile.read(int(self.headers["Content-Length"]))  # byte string
            data_parse = urllib.parse.unquote_plus(data.decode("utf-8"))  # decoded str
            data_dict = {
                key: value
                for key, value in [el.split("=") for el in data_parse.split("&")]
            }  # dict with parsed data

            asyncio.run(self.send_message(json.dumps(data_dict)))

            self.send_response(302)
            self.send_header("Location", "/")  # redirection to the main page
            self.end_headers()
        else:
            self.send_html_file("templates/error.html", 404)

    def do_GET(self):
        """
        Method that provides routing by handling GET requests to the HTTP server
        """
        pr_url = urllib.parse.urlparse(self.path)
        if pr_url.path == "/":
            self.send_html_file("templates/index.html")
        elif pr_url.path == "/message":
            self.send_html_file("templates/message.html")
        else:
            if pathlib.Path().joinpath(pr_url.path[1:]).exists():
                self.send_static()
            else:
                self.send_html_file("templates/error.html", 404)

    def send_html_file(self, filename: str, status: int = 200):
        """
        Method that sends html files to the client as response from the HTTP server

        :param filename: Name of the html page to send
        :status: Response status code
        """
        self.send_response(status)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        with open(filename, "rb") as fd:
            self.wfile.write(fd.read())

    def send_static(self):
        """
        Method that sends static resouces to the client
        """
        self.send_response(200)
        mime_type = mimetypes.guess_type(self.path)
        if mime_type:
            self.send_header("Content-type", mime_type[0])
        else:
            self.send_header("Content-type", "text/plain")
        self.end_headers()
        with open(f".{self.path}", "rb") as file:
            self.wfile.write(file.read())


def run_http_server(server_class=HTTPServer, handler_class=HttpHandler):
    """
    Function that runs HTTP server

    :param server_class: Class of the server
    :param handler_class: Class that handles all requests to the server
    """
    server_address = (HTTP_SERVER_HOST, HTTP_SERVER_PORT)
    http = server_class(server_address, handler_class)
    try:
        logging.info(
            "HTTP server is running at 'http://%s:%s/'",
            HTTP_SERVER_HOST,
            HTTP_SERVER_PORT,
        )
        http.serve_forever()
    except KeyboardInterrupt:
        http.server_close()
        logging.info("HTTP server is interrupted")


class SocketHandler:
    """
    Class that handles all requests to Socket server
    """

    async def message_handler(self, message: str):
        """
        Asynchronous function that handles interactions with database
        """
        db_collection = await provide_db_collection()

        message_dict = json.loads(message)
        message_dict["date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        result = await db_collection.insert_one(message_dict)
        logging.info("Message is inserted to DB with ID: %s", result)

    async def websocket_handler(self, websocket):
        """
        Asynchronous function that handles messages on websockets
        """
        message = await websocket.recv()
        await self.message_handler(message)


async def run_socket_server(handler_class=SocketHandler):
    """
    Asynchronous function that runs Socket server that interacts with database
    """
    try:
        socket_server = handler_class()
        async with websockets.serve(
            socket_server.websocket_handler, SOCKET_SERVER_HOST, SOCKET_SERVER_PORT
        ):
            logging.info("Socket server is listening on port %s", SOCKET_SERVER_PORT)
            await asyncio.Future()
    except (KeyboardInterrupt, asyncio.exceptions.CancelledError):
        logging.info("Socket server is interrupted")


if __name__ == "__main__":
    http_server_process = Process(target=run_http_server)
    http_server_process.start()

    asyncio.run(run_socket_server())

    http_server_process.join()

    logging.info("Both servers are interrupted")
