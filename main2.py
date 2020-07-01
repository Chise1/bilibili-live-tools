from aioweb import WebClient
import asyncio

if __name__ == '__main__':
    client = WebClient()
    asyncio.run(client.receive())

