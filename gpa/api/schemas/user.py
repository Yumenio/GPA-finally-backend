from ninja import Schema
from django.contrib.auth.models import User


class UserCreateSchema(Schema):
    username: str
    password: str


class UserUpdateSchema(Schema):
    password: str


class LoginCredentials(Schema):
    username: str
    password: str
