from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from authorization_app.serializers import CreateUserSerializer, UpdateUserSerializer
from authorization_app.serializers import ValidateUserSerializer
from authorization_app.serializers import CreateDataOwnershipSerializer
from authorization_app.serializers import MatchDataOwnershipSerializer
from django.views.decorators.csrf import csrf_exempt
from authorization_app.models.user import User
import json


@csrf_exempt
def create_user(request):
    response = {"status": "failed"}
    if request.method == "POST":
        serializer = CreateUserSerializer(data=request.POST)
        if serializer.is_valid():
            response = serializer.create(serializer.validated_data)
            response["status"] = "success"
    return JsonResponse(response, safe=False)


@csrf_exempt
def change_settings(request):
    response = {"status": "failed"}
    if request.method == "POST":
        serializer = UpdateUserSerializer(data=request.POST)
        if serializer.is_valid():
            try:
                user = User.objects.get(
                    id=request.POST.get('id', -1),
                    auth_token=request.POST.get('auth_token', '')
                )
                user.name = request.POST.get('name', '')
                user.email = request.POST.get('email', '')
                user.meta = request.POST.get('meta', '')
                user.save()
                response["status"] = "success"
            except User.DoesNotExist as e:
                pass
    return JsonResponse(response, safe=False)


@csrf_exempt
def post_data(request):
    # Inside API
    response = {"status": "failed"}
    if request.method == "POST":
        data = {
            "id": request.POST.get('id', -1),
            "auth_token": request.POST.get('auth_token', '')
        }
        serializer = ValidateUserSerializer(data=data)
        if serializer.is_valid():
            try:
                user = User.objects.get(
                    id=request.POST.get('id', -1),
                    auth_token=request.POST.get('auth_token', '')
                )
                serializer_owner = CreateDataOwnershipSerializer(
                    data={
                        "id_owner": user.id,
                        "id_data_value": request.POST.get('id_data_value', ''),
                        "data_type": request.POST.get('data_type', ''),
                        "timestamp": request.POST.get('timestamp', 0),
                    }
                )
                if serializer_owner.is_valid():
                    status = serializer_owner.create(
                        serializer_owner.validated_data
                    )
                    response["status"] = "success" if status else "failed"
            except User.DoesNotExist as e:
                pass
    return JsonResponse(response, safe=False)


def validate_user(request):
    # Inside API
    response = {"status": "failed"}
    try:
        serializer = ValidateUserSerializer(data=request.GET)
        if serializer.is_valid():
            user = User.objects.get(
                id=request.GET.get('id', -1),
                auth_token=request.GET.get('auth_token', '')
            )
            response["status"] = "success"
    except User.DoesNotExist as e:
        pass
    return JsonResponse(response, safe=False)


def match_data(request):
    response = {"status": "failed"}
    validate_status = json.loads(
        validate_user(request).content.decode("utf-8")
    )
    if validate_status["status"] == "success":
        cur_id = request.GET.get('id')
        serializer = MatchDataOwnershipSerializer()
        response_data = serializer.to_internal_value(cur_id)
        if response_data:
            response = {
                "status": "success",
                **response_data
            }
    return JsonResponse(response, safe=False)
