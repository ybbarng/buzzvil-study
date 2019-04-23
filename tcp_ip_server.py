#!/usr/bin/env python3
import asyncio
import os

from echo_server import EchoServer
from http_server import HttpServer


def get_ip():
    return os.popen('ifconfig en0 | grep "inet\ " | cut -d: -f2 -d\' \'').read().strip()


def run_server(server_class, host, port, n_client=30):
    loop = asyncio.get_event_loop()
    coro = loop.create_server(server_class, host, port)
    server = loop.run_until_complete(coro)
    ip = get_ip()
    print(f'Server is running at {ip}:{port}')
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        print('Stop signal is received')
    finally:
        server.close()
        loop.run_until_complete(server.wait_closed())
        loop.close()
        print('Server is shutdown')


if __name__ == '__main__':
    print('Choose TCP/IP server mode:')
    print('   1) Echo Server')
    print('   2) HTTP Server')
    mode = input()
    if mode == '1':
        print('\'Echo Server\' mode is selected.')
        run_server(EchoServer, '0.0.0.0', 1234)
    if mode == '2':
        print('\'HTTP Server\' mode is selected.')
        run_server(HttpServer, '0.0.0.0', 80)
