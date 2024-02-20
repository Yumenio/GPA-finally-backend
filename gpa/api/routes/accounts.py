from django.db.utils import IntegrityError
from django.contrib.auth.models import User
from django.http import (
    HttpResponseServerError,
    JsonResponse,
    HttpResponseNotFound,
    HttpResponseForbidden,
)
from django.shortcuts import get_object_or_404
from ninja import Router

from api.schemas.account import AccountCreateSchema, AccountUpdateSchema
from api.models.account import Account
from api.utils import AuthBearer, to_dict

router = Router()


@router.post("create", response={201: None})
def create_account(request, account: AccountCreateSchema):
    try:
        new_account = Account(**account.model_dump())
        new_account.save()
    except IntegrityError:
        return HttpResponseNotFound("User not found")
    except Exception as e:
        return HttpResponseServerError(f"An error ocurred: {str(e)}")


@router.get("{id}")
def get_account(request, id):
    account = get_object_or_404(Account, ID=id)
    return to_dict(account)


@router.get("/user/{user_id}", auth=AuthBearer())
def get_account_by_user_id(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.auth["user_id"] != user.id:
        return HttpResponseForbidden("Invalid credentials")
    accounts = Account.objects.filter(user_id=user_id)
    return [to_dict(acc) for acc in accounts]


@router.get("", response={200: None})
def get_all_accounts(request):
    return JsonResponse(list(Account.objects.all().values()), safe=False)


@router.put("{id}", response={201: None})
def update_account(request, id, accountData: AccountUpdateSchema):
    account = get_object_or_404(Account, ID=id)
    account.current_balance = accountData.current_balance
    account.save()


@router.delete("{id}", response={204: None})
def delete_account(request, id):
    account = get_object_or_404(Account, ID=id)
    account.delete()
