import jwt
from django.conf import settings
from django.db import transaction
from django.shortcuts import get_object_or_404
from ninja import Router
from django.contrib.auth import authenticate
from django.http import JsonResponse, HttpResponseServerError, HttpResponseNotFound
from django.contrib.auth.models import User
from django.db.utils import IntegrityError

from api.schemas.user import LoginCredentials, UserCreateSchema

router = Router()


def generate_token(user):
    return jwt.encode({"user_id": user.id}, settings.SECRET_KEY, algorithm="HS256")


def authenticate_user(request, username, password):
    user = authenticate(request, username=username, password=password)
    if user is None:
        raise HttpResponseNotFound("Invalid credentials")
    return user


@router.post("register")
def register_user(request, user: UserCreateSchema):
    try:
        with transaction.atomic():
            user = User.objects.create_user(
                username=user.username, password=user.password
            )
            token = generate_token(user)
            return {"user_id": user.id, "token": token}
    except IntegrityError:
        return HttpResponseServerError("Username already exists")
    except Exception as e:
        return HttpResponseServerError(f"An error ocurred: {str(e)}")


@router.post("login")
def login_user(request, credentials: LoginCredentials):

    user_login = authenticate(
        request, username=credentials.username, password=credentials.password
    )
    if user_login:
        user = User.objects.filter(username=credentials.username).first()
        token = generate_token(user)
        return {"user_id": user.id, "token": token}
    else:
        return HttpResponseNotFound("Invalid credentials")


@router.get("")
def get_all_users(request):
    return JsonResponse(list(User.objects.all().values()), safe=False)


@router.delete("{id}", response={204: None})
def delete_user(request, id):
    account = get_object_or_404(User, id=id)
    account.delete()
