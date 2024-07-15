# main.py
import socket
from typing import overload


class TCPServer:
    def __init__(self, host="127.0.0.1", port="8080") -> None:
        self.host = host
        self.port = 8080

    def start(self):
        # create an IPV4 socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((self.host, self.port))
        s.listen(5)

        print(f"Started to listen at {s.getsockname()}")

        while True:
            conn, addr = s.accept()
            print(f"Connected by {addr}")
            data = conn.recv(10000000)
            response = self.handle_request(data)
            conn.sendall(response)
            conn.close()

    @overload
    def handle_request(self, data):
        raise NotImplementedError('This method has to be overloaded!!!')


class HTTPServer(TCPServer):

    def handle_request(self, data):
        response_line = b"HTTP/1.1 200 OK"
        blank_line = b"\r\n"
        headers = b"".join([
            b"Server: Ishanu's Echo Server", blank_line,
            b"Content-Type: text/html", blank_line
        ])

        response_body = b"""
        <html>
            <h1>
                Request Received !!!
            </h1>
            <h2> 
                Request Body
            </h2>
            <div> %s </div>
        </html>
        """ % data

        return b"".join([response_line, blank_line, headers,  blank_line, response_body])


if __name__ == "__main__":
    server = HTTPServer()
    server.start()
