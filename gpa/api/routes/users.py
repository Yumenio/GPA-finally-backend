from django.shortcuts import get_object_or_404
from ninja import Router
from django.http import (
    JsonResponse,
    HttpResponseServerError,
)
from django.contrib.auth.models import User
from django.db.utils import IntegrityError

from api.schemas.user import UserCreateSchema

router = Router()


@router.post("create")
def register_user(request, user: UserCreateSchema):
    try:
        new_user = User(**user.model_dump())
        new_user.save()
    except IntegrityError:
        return HttpResponseServerError(f"Username already exists")
    except Exception as e:
        return HttpResponseServerError(f"An error ocurred: {str(e)}")
    return {"created_user": user}


@router.get("")
def get_all_users(request):
    return JsonResponse(list(User.objects.all().values()), safe=False)


@router.delete("{id}", response={204: None})
def delete_user(request, id):
    account = get_object_or_404(User, id=id)
    account.delete()
