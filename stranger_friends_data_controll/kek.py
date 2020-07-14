from tornado.httpclient import AsyncHTTPClient
from tornado.ioloop import IOLoop

AsyncHTTPClient.configure(None, defaults=dict(user_agent="MyUserAgent"))
http_client = AsyncHTTPClient()

import sys


def handle_response(response):
    if response.error:
        print("Error: %s" % response.error, file=sys.stderr, flush=True)
    else:
        print(response, response.body, file=sys.stderr, flush=True)
    return response


async def get_content():
    return await http_client.fetch("http://127.0.0.1:8000/authorization/kek", handle_response)


async def main():
    response = await get_content()
    print(type(response), file=sys.stderr, flush=True)
    print(response, response.body, response.code, file=sys.stderr, flush=True)

if __name__ == "__main__":
    io_loop = IOLoop.current()
    io_loop.run_sync(main)
