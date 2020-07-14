from rest_framework import serializers
from authorization_app.models.user import User
from authorization_app.models.data_ownership import DataOwnership
from django.utils.crypto import get_random_string
from random import randint


class CreateDataOwnershipSerializer(serializers.ModelSerializer):

    class Meta:
        model = DataOwnership
        fields = ('id_owner', 'id_data_value', 'data_type', 'timestamp')

    def create(self, validated_data):
        data_ownership = DataOwnership(
            id_owner=validated_data['id_owner'],
            id_data_value=validated_data['id_data_value'],
            data_type=validated_data['data_type'],
            timestamp=validated_data['timestamp']
        )
        data_ownership.save()
        return True


class MatchDataOwnershipSerializer(serializers.ModelSerializer):

    class Meta:
        model = DataOwnership
        fields = '__all__'

    def to_internal_value(self, id):
        objects_count = DataOwnership.objects.exclude(id_owner=id).count()
        if objects_count:
            row_data = DataOwnership.objects.exclude(
                id_owner=id
            )[randint(0, objects_count - 1)]
            return {
                "id_owner": row_data.id_owner.id,
                "id_data_value": row_data.id_data_value,
            }
        return None


class CreateUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('name', 'email', 'meta')

    def create(self, validated_data):
        user = User(
            auth_token=get_random_string(32),
            name=validated_data['name'],
            email=validated_data['email'],
            meta=validated_data['meta'],
        )
        user.save()
        response = {
            "auth_token": user.auth_token,
            "id": user.id
        }
        return response


class UpdateUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'


class ValidateUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'auth_token')
