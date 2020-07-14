import unittest
import asyncio

import sys

from unittest import TestCase
from unittest import mock

from tornado.options import define, options, parse_command_line
from tornado.httpclient import AsyncHTTPClient, HTTPResponse, HTTPRequest
from data_controll import UserManipulator

AUTHORIZATION_SERVER_VALIDATE_USER_URL = (
    'http://localhost:8000/authorization/validate_user'
)
AUTHORIZATION_SERVER_POST_DATA_URL = (
    'http://localhost:8000/authorization/post_data'
)
ID = 1
AUTH_TOKEN = "AUTH TOKEN"
ID_DATA_VALUE = "ID DATA VALUE"

CHECK_URL = AUTHORIZATION_SERVER_VALIDATE_USER_URL + \
    f"?id={ID}&auth_token={AUTH_TOKEN}"

POST_URL = AUTHORIZATION_SERVER_POST_DATA_URL + \
    f"?id={ID}&auth_token={AUTH_TOKEN}" + \
    f"&id_data_value={ID_DATA_VALUE}"


async def mocked_requests(*args, **kwargs):
    response = HTTPResponse(HTTPRequest("kek"), 200)
    response._body = {"status": "success"}
    response.buffer = "trash"
    return response


class BaseTestClass():

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.define_options()

    def define_options(self):
        define('port', default=9000, type=int, help='Port')
        define('instances', default=1, type=int, help='Instance number')
        define('dev_mode', default=True, type=bool, help='Dev mode')
        define(
            'authorization_server_validate_user_url',
            default=AUTHORIZATION_SERVER_VALIDATE_USER_URL,
            help="Authorization server's validate user url"
        )
        define(
            'authorization_server_post_data_url',
            default=AUTHORIZATION_SERVER_POST_DATA_URL,
            help="Authorization server's post data url"
        )
        define('db_port', default=27017, type=int, help='Data base port')
        define('db_host', default='localhost', help='Data base host')
        define('db_name', default='data', help='Data base name')
        define(
            'db_collection', default='collection',
            help='Data collection name'
        )
        parse_command_line()


class TestData_controll(BaseTestClass, TestCase):

    @mock.patch('tornado.httpclient.AsyncHTTPClient.fetch', side_effect=mocked_requests)
    def test_UserManipulator(self, mock_get):
        self.assertTrue(True)
        user = UserManipulator()
        status = asyncio.run(user.check_user(ID, AUTH_TOKEN))
        self.assertTrue(status)
        status = asyncio.run(
            user.post_id_data_value(ID, AUTH_TOKEN, ID_DATA_VALUE)
        )


if __name__ == '__main__':
    unittest.main()
