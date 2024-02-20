from ninja import Schema


class UserCreateSchema(Schema):
    username: str
    password: str


class UserUpdateSchema(Schema):
    password: str


class LoginCredentials(Schema):
    username: str
    password: str
