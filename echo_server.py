import asyncio


class EchoServer(asyncio.Protocol):
    def connection_made(self, transport):
        self.peername = transport.get_extra_info('peername')
        self.transport = transport
        print(f'{self.peername} is connected.')

    def data_received(self, data):
        received = data.decode()
        print(f'{self.peername} >> {received}')
        response = f'<EchoServer> Hey you said: {received}'
        self.transport.write(response.encode())
        print(f'{self.peername} << {response}')


