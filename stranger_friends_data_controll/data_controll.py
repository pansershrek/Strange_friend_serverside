import logging
import json
import datetime


import tornado.gen
import tornado.ioloop
from tornado.httpserver import HTTPServer
from tornado.httpclient import AsyncHTTPClient
from tornado.web import RequestHandler, Application
from tornado.options import define, options, parse_config_file

from motor.motor_tornado import MotorClient
from bson.objectid import ObjectId


class UserManipulator():

    async def check_user(self, id, auth_token):
        # Remove this return
        # return True
        try:
            http_client = AsyncHTTPClient()
            url = options.authorization_server_validate_user_url + \
                f"?id={id}&auth_token={auth_token}"
            response = await http_client.fetch(url)
            return response.code == 200 and response.body["status"] == "success"
        except BaseException as e:
            logging.error(f"Could not check user with {e}")
        return False

    async def post_id_data_value(
        self, id, auth_token, id_data_value, data_type="", timestamp=0
    ):
        try:
            http_client = AsyncHTTPClient()
            url = options.authorization_server_post_data_url + \
                f"?id={id}&auth_token={auth_token}" + \
                f"&id_data_value={id_data_value}" + \
                f"&data_type={data_type}" + \
                f"&timestamp={timestamp}"
            response = await http_client.fetch(url, method='POST')
            return response.code == 200 and response.body["status"] == "success"
        except BaseException as e:
            logging.error(f"Could not post id_data_value with {e}")
        return False


class BaseHandler(RequestHandler):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_request_params(self):
        self.id = self.get_argument("id", None, strip=True)
        self.auth_token = self.get_argument("auth_token", None, strip=True)

    def get_id_data_value(self):
        self.id_data_value = self.get_argument("id_data_value", None)

    def get_data(self):
        self.data = self.get_argument("data", None)
        self.data_type = self.get_argument("data_type", "")
        self.timestamp = datetime.datetime.now().timestamp()


class GetDataHandler(BaseHandler, UserManipulator):

    async def get(self):
        responce = {"status": "failed"}
        self.get_request_params()
        if await self.check_user(self.id, self.auth_token):
            self.get_id_data_value()
            try:
                mongo_data = await self.settings['db'][options.db_collection].find_one(
                    {'_id': ObjectId(self.id_data_value)}
                )
                responce = {
                    "status": "success",
                    "data": mongo_data.get("data", ""),
                }
            except BaseException as e:
                logging.info(e)
        self.finish(json.dumps(responce, ensure_ascii=False))


class PostDataHandler(UserManipulator, BaseHandler):

    async def post(self):
        responce = {"status": "failed"}
        self.get_request_params()
        if await self.check_user(self.id, self.auth_token):
            self.get_data()
            try:
                result = await self.settings['db'][options.db_collection].insert_one(
                    {"data": self.data}
                )
                if await self.post_id_data_value(
                    self.id, self.auth_token, self.id_data_value,
                    self.data_type, self.timestamp
                ):
                    responce = {
                        "status": "success",
                        "id_data_value": str(result.inserted_id)
                    }
            except BaseException as e:
                logging.info(e)

        self.finish(json.dumps(responce, ensure_ascii=False))


class DataControllApp():

    def __init__(self):
        self.define_options()
        self.run()

    def define_options(self):
        define('port', default=9000, type=int, help='Port')
        define('instances', default=1, type=int, help='Instance number')
        define('dev_mode', default=True, type=bool, help='Dev mode')
        define(
            'authorization_server_validate_user_url', default='',
            help="Authorization server's validate user url"
        )
        define(
            'authorization_server_post_data_url', default='',
            help="Authorization server's post data url"
        )
        define('db_port', default=27017, type=int, help='Data base port')
        define('db_host', default='localhost', help='Data base host')
        define('db_name', default='data', help='Data base name')
        define(
            'db_collection', default='collection',
            help='Data collection name'
        )

        parse_config_file('etc/data_controll.ini.default')

    @staticmethod
    def make_tornado_app(project_options):
        settings = {
            "debug": project_options.dev_mode,
        }

        http_app = Application([
            tornado.web.url(r"/get_data", GetDataHandler, name="get_data"),
            tornado.web.url(r"/post_data", PostDataHandler, name="post_data"),
        ], **settings)

        http_app.options = project_options
        return http_app

    def run(self):
        try:
            app = self.make_tornado_app(options)
        except BaseException as e:
            logging.exception(e)
            exit(1)

        logging.info(f"HTTP Server started on port: {options.port}")
        try:
            server = HTTPServer(app)
            server.bind(options.port)

            if options.dev_mode and options.instances > 1:
                logging.critical("You can't run in paralell in dev mode")
                server.start()
            else:
                server.start(options.instances)

            app.settings['db'] = MotorClient(
                options.db_host, options.db_port
            )[options.db_name]
            ioloop = tornado.ioloop.IOLoop.current().start()
        except KeyboardInterrupt:
            logging.critical("User interrupt")

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    app = DataControllApp()
