from django.test import TestCase
from authorization_app.models.user import User
from authorization_app.models.data_ownership import DataOwnership
from django.utils.crypto import get_random_string
from authorization_app.serializers import *


class UserSerializersTestCase(TestCase):
    AUTH_TOKEN = get_random_string(32)
    NAME = "TEST USER"
    EMAIL = "TEST_EMAIL@MAILR.RU"
    META = "TEST USER META"
    ID_DATA_VALUE = "ID DATA VALUE"

    def test_create_user(self):
        test_case = "CREATE"
        serializer = CreateUserSerializer(
            data={
                'name': self.NAME + test_case,
                'email': self.EMAIL + test_case,
                'meta': self.META + test_case,
            }
        )
        self.assertTrue(serializer.is_valid())
        response = serializer.create(
            serializer.validated_data
        )
        self.assertTrue(bool(response))

    def test_update1_user(self):
        data = {
            'id': -1,
            'auth_token': 'invalid_token',
        }
        serializer = UpdateUserSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_update2_user(self):
        test_case = "UPDATE2"
        serializer = CreateUserSerializer(
            data={
                'name': self.NAME + test_case,
                'email': self.EMAIL + test_case,
                'meta': self.META + test_case,
            }
        )
        self.assertTrue(serializer.is_valid())
        response = serializer.create(
            serializer.validated_data
        )
        self.assertTrue(bool(response))

        data1 = {
            'id': response['id'],
            'auth_token': response['auth_token'],
            'name': self.NAME,
            'email': self.EMAIL,
            'meta': self.META
        }
        serializer_update = UpdateUserSerializer(data=data1)
        self.assertTrue(serializer.is_valid())

    def test_validate_user(self):
        data = {
            'id': -1,
            'auth_token': 'invalid_token',
        }
        serializer = ValidateUserSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_create_ownership(self):
        test_case = "CREATE"
        serializer = CreateUserSerializer(
            data={
                'name': self.NAME + test_case,
                'email': self.EMAIL + test_case,
                'meta': self.META + test_case,
            }
        )
        self.assertTrue(serializer.is_valid())
        response = serializer.create(
            serializer.validated_data
        )
        self.assertTrue(bool(response))
        data1 = {
            'id_owner': response['id'],
            'id_data_value': self.ID_DATA_VALUE,
            'data_type': 'test_data',
            'timestamp': 0,
        }
        serializer_own = CreateDataOwnershipSerializer(
            data=data1
        )
        self.assertTrue(serializer_own.is_valid())
        self.assertTrue(
            serializer_own.create(serializer_own.validated_data)
        )

    def test_data_match(self):
        test_case = "MATCH"
        # First user and it's data
        serializer1 = CreateUserSerializer(
            data={
                'name': self.NAME + test_case,
                'email': self.EMAIL + test_case,
                'meta': self.META + test_case,
            }
        )
        self.assertTrue(serializer1.is_valid())
        response1 = serializer1.create(
            serializer1.validated_data
        )
        self.assertTrue(bool(response1))
        data1 = {
            'id_owner': response1['id'],
            'id_data_value': self.ID_DATA_VALUE + "1",
            'data_type': 'test_data',
            'timestamp': 0,
        }
        serializer_own1 = CreateDataOwnershipSerializer(
            data=data1
        )
        self.assertTrue(serializer_own1.is_valid())
        self.assertTrue(
            serializer_own1.create(serializer_own1.validated_data)
        )

        # Second user and it's data

        serializer2 = CreateUserSerializer(
            data={
                'name': self.NAME + test_case + "2",
                'email': self.EMAIL + test_case + "2",
                'meta': self.META + test_case + "2",
            }
        )
        self.assertTrue(serializer2.is_valid())
        response2 = serializer2.create(
            serializer2.validated_data
        )
        self.assertTrue(bool(response2))
        data2 = {
            'id_owner': response2['id'],
            'id_data_value': self.ID_DATA_VALUE + "2",
            'data_type': 'test_data',
            'timestamp': 0,
        }
        serializer_own2 = CreateDataOwnershipSerializer(
            data=data2
        )
        self.assertTrue(serializer_own2.is_valid())
        self.assertTrue(
            serializer_own2.create(serializer_own2.validated_data)
        )
        # Matching
        match_serializer = MatchDataOwnershipSerializer()
        match_result = match_serializer.to_internal_value(response1['id'])
        self.assertNotEqual(
            None, match_result
        )

        self.assertEqual(response2['id'], match_result["id_owner"])
        self.assertEqual(data2['id_data_value'], match_result["id_data_value"])
