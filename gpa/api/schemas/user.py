from ninja import ModelSchema
from django.contrib.auth.models import User


class UserSchema(ModelSchema):
    class Meta:
        model = User
        fields = ["username"]


class UserCreateSchema(UserSchema):
    pass


class UserUpdateSchema(UserSchema):
    pass
