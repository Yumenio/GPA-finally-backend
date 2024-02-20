from ninja import Router
from django.db import transaction as transaction_manager
from django.shortcuts import get_object_or_404
from django.db.utils import IntegrityError
from django.contrib.auth.models import User
from django.http import HttpResponseServerError, JsonResponse, HttpResponseForbidden

from api.models.account import Account
from api.models.transaction import Transaction
from api.schemas.transaction import (
    TransactionTypes,
    TransactionCreateSchema,
    TransactionUpdateSchema,
)
from api.utils import AuthBearer, to_dict

router = Router()


@router.post("create/", response={201: None})
def create_transaction(request, transaction: TransactionCreateSchema):
    owner_account = get_object_or_404(Account, ID=transaction.account_id)
    transaction.transaction_type = (
        "CREDIT" if transaction.transaction_type == TransactionTypes.credit else "DEBIT"
    )

    try:
        amount = (
            transaction.amount
            if transaction.transaction_type == "DEBIT"
            else -transaction.amount
        )
        # since we are creating/modifying two db entries, we should rollback if anything goes wrong
        with transaction_manager.atomic():
            new_transaction = Transaction(
                account=owner_account, **transaction.model_dump()
            )
            new_transaction.save()

            # amount will be negative if transaction_type is CREDIT
            owner_account.current_balance += amount
            # do we wanna have accounts with negative balance?
            if owner_account.current_balance < 0:
                raise Exception("Not enough funds")
            owner_account.save()
    except IntegrityError:
        pass
    except Exception as e:
        return HttpResponseServerError(f"An error ocurred: {str(e)}")


@router.get("{id}", auth=AuthBearer())
def get_transaction(request, id):
    # check that transaction exists
    transaction = get_object_or_404(Transaction, ID=id)
    # check who owns the transaction
    owner = Account.objects.filter(ID=transaction.account_id).first().user_id
    # check that jwt token was issued to the owner of this transaction
    if request.auth["user_id"] != owner:
        return HttpResponseForbidden("User doesn't own the account of that transaction")
    return to_dict(transaction)


@router.get("/account/{account_id}", auth=AuthBearer())
def get_transactions_by_account(request, account_id):
    account = get_object_or_404(Account, ID=account_id)
    owner = User.objects.get(id=account.user.id)
    if request.auth["user_id"] != owner.id:
        return HttpResponseForbidden("User doesn't own the account of that transaction")
    transactions = Transaction.objects.filter(account_id=account_id).order_by("date")
    return [to_dict(t) for t in transactions]


@router.get("")
def get_all_transactions(request):
    return JsonResponse(list(Transaction.objects.all().values()), safe=False)


# I'm not sure wether updating a transaction should be allowed
@router.put("{id}")
def update_transaction(request, id, transactionData: TransactionUpdateSchema):
    raise NotImplementedError()


# Same as for updating a transaction
@router.delete("{id}")
def delete_transaction(request, id):
    raise NotImplementedError()
