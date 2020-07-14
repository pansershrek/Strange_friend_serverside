from django.test import TestCase, Client
from django.urls import reverse
from authorization_app.views.views import *
import json


class ViewsTestCase(TestCase):
    NAME = "TEST USER"
    EMAIL = "TEST_EMAIL@MAILR.RU"
    META = "TEST USER META"
    BASIC_URL = "authorization"
    ID_DATA_VALUE = "ID DATA VALUE"
    URLS = [
        "create_user", "change_settings",
        "post_data", "validate_user", "match_data"
    ]

    def setUp(self):
        self.client = Client()

    def create_url(self, url_part):
        return "http://localhost:8000/" + self.BASIC_URL + "/" + url_part

    def test_create_user(self):
        response = self.client.post(
            self.create_url(self.URLS[0]),
            {'name': self.NAME, 'email': self.EMAIL, 'meta': self.META}
        )
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content.decode("utf-8"))
        self.assertEqual(
            response_data["status"], "success"
        )

    def test_change_settings(self):
        test_case = "CHANGE"
        response = self.client.post(
            self.create_url(self.URLS[0]),
            {'name': self.NAME, 'email': self.EMAIL, 'meta': self.META}
        )
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content.decode("utf-8"))
        self.assertEqual(
            response_data["status"], "success"
        )
        response_data.pop("status")
        response_new = self.client.post(
            self.create_url(self.URLS[1]),
            {
                **response_data,
                'name': self.NAME + test_case,
                'email': self.EMAIL + test_case,
                'meta': self.META + test_case,
            }
        )
        self.assertEqual(response_new.status_code, 200)
        response_new_data = json.loads(response_new.content.decode("utf-8"))
        self.assertEqual(
            response_new_data["status"], "success"
        )

    def test_post_data(self):
        test_case = "POST DATA"
        response = self.client.post(
            self.create_url(self.URLS[0]),
            {'name': self.NAME, 'email': self.EMAIL, 'meta': self.META}
        )
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content.decode("utf-8"))
        self.assertEqual(
            response_data["status"], "success"
        )
        response_data.pop("status")
        response_new = self.client.post(
            self.create_url(self.URLS[2]),
            {
                **response_data,
                "id_data_value": self.ID_DATA_VALUE + "VIEW",
                "data_type": "test_data",
                "timestamp": 0,
            }
        )
        self.assertEqual(response_new.status_code, 200)
        response_new_data = json.loads(response_new.content.decode("utf-8"))
        self.assertEqual(
            response_new_data["status"], "success"
        )

    def test_validate_user(self):
        response = self.client.post(
            self.create_url(self.URLS[0]),
            {'name': self.NAME, 'email': self.EMAIL, 'meta': self.META}
        )
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content.decode("utf-8"))
        self.assertEqual(
            response_data["status"], "success"
        )
        response_data.pop("status")
        response_new = self.client.get(
            self.create_url(self.URLS[3]),
            {
                **response_data,
            }
        )
        self.assertEqual(response_new.status_code, 200)
        response_new_data = json.loads(response_new.content.decode("utf-8"))
        self.assertEqual(
            response_new_data["status"], "success"
        )

    def test_match(self):
        test_case = "POST DATA"
        # Post user 1
        response = self.client.post(
            self.create_url(self.URLS[0]),
            {'name': self.NAME + "1", 'email': self.EMAIL, 'meta': self.META}
        )
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content.decode("utf-8"))
        self.assertEqual(
            response_data["status"], "success"
        )
        response_data.pop("status")
        response_new = self.client.post(
            self.create_url(self.URLS[2]),
            {
                **response_data,
                "id_data_value": self.ID_DATA_VALUE + "VIEW 1",
                "data_type": "test_data",
                "timestamp": 0,
            }
        )
        self.assertEqual(response_new.status_code, 200)
        response_new_data = json.loads(response_new.content.decode("utf-8"))
        self.assertEqual(
            response_new_data["status"], "success"
        )
        # Post user 2
        response = self.client.post(
            self.create_url(self.URLS[0]),
            {'name': self.NAME + "2", 'email': self.EMAIL, 'meta': self.META}
        )
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content.decode("utf-8"))
        self.assertEqual(
            response_data["status"], "success"
        )
        response_data.pop("status")
        response_new = self.client.post(
            self.create_url(self.URLS[2]),
            {
                **response_data,
                "id_data_value": self.ID_DATA_VALUE + "VIEW ",
                "data_type": "test_data",
                "timestamp": 0,
            }
        )
        self.assertEqual(response_new.status_code, 200)
        response_new_data = json.loads(response_new.content.decode("utf-8"))
        self.assertEqual(
            response_new_data["status"], "success"
        )

        response_match = self.client.get(
            self.create_url(self.URLS[4]),
            {**response_data}
        )
        response_match_data = json.loads(
            response_match.content.decode("utf-8")
        )
        self.assertNotEqual(
            self.ID_DATA_VALUE + "VIEW ", response_match_data["id_data_value"]
        )
