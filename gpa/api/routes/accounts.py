from django.db.utils import IntegrityError
from django.http import HttpResponseServerError, JsonResponse, HttpResponseNotFound
from django.shortcuts import get_object_or_404
from ninja import Router

from api.schemas.account import AccountCreateSchema, AccountUpdateSchema
from api.models.account import Account
from api.utils import to_dict

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
