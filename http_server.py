import asyncio


class HttpServer(asyncio.Protocol):

    def connection_made(self, transport):
        self.peername = transport.get_extra_info('peername')
        self.transport = transport
        print(f'{self.peername} is connected.')

    def data_received(self, data):
        received = data.decode()
        print(f'{self.peername} >> {received}')

        if received.lower().startswith('get /index.html'):
            response = self.get_index_html()

        self.transport.write(response.encode())
        print(f'{self.peername} << html is sent')

    def get_index_html(self):
        with open('index.html') as f:
            return f.read()

