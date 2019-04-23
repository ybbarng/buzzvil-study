#!/usr/bin/env python3
import asyncio
import os


class EchoServer(asyncio.Protocol):
    def connection_made(self, transport):
        self.peername = transport.get_extra_info('peername')
        self.transport = transport
        print(f'{self.peername} is connected.')

    def data_received(self, data):
        received = data.decode()
        print(f'{self.peername} >> {received}')
        response = f'Hey you said: {received}'
        self.transport.write(response.encode())
        print(f'{self.peername} << {response}')


def get_ip():
    return os.popen('ifconfig en0 | grep "inet\ " | cut -d: -f2 -d\' \'').read().strip()


def run_server(host, port, n_client=30):
    loop = asyncio.get_event_loop()
    coro = loop.create_server(EchoServer, host, port)
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
    run_server('0.0.0.0', 1234)
