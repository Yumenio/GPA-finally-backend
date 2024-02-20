from jwt import decode
from itertools import chain
from django.conf import settings
from ninja.security import HttpBearer


def to_dict(instance):
    opts = instance._meta
    data = {}
    for f in chain(opts.concrete_fields, opts.private_fields):
        data[f.name] = f.value_from_object(instance)
    for f in opts.many_to_many:
        data[f.name] = [i.id for i in f.value_from_object(instance)]
    return data


class AuthBearer(HttpBearer):
    def authenticate(self, request, token):
        return decode(token, settings.SECRET_KEY, "HS256")
