from ninja import Router
from django.shortcuts import get_object_or_404
from django.db.utils import IntegrityError
from django.http import HttpResponseServerError, JsonResponse

from api.models.account import Account
from api.models.transaction import Transaction
from api.schemas.transaction import (
    TransactionTypes,
    TransactionCreateSchema,
    TransactionUpdateSchema,
)
from api.utils import to_dict

router = Router()


@router.post("create/", response={201: None})
def create_transaction(request, transaction: TransactionCreateSchema):
    owner_account = get_object_or_404(Account, ID=transaction.account_id)
    transaction.transaction_type = (
        "CREDIT" if transaction.transaction_type == TransactionTypes.credit else "DEBIT"
    )

    try:
        new_transaction = Transaction(account=owner_account, **transaction.model_dump())
        print(new_transaction)
        new_transaction.save()

        # amount will be negative if transaction_type is CREDIT
        amount = (
            transaction.amount
            if transaction.transaction_type == "DEBIT"
            else -transaction.amount
        )
        owner_account.current_balance += amount
        owner_account.save()
    except IntegrityError:
        pass
    except Exception as e:
        return HttpResponseServerError(f"An error ocurred: {str(e)}")


@router.get("{id}")
def get_transaction(request, id):
    transaction = get_object_or_404(Transaction, ID=id)
    return to_dict(transaction)


@router.get("/account/{account_id}")
def get_transactions_by_account(request, account_id):
    get_object_or_404(Account, ID=account_id)
    transactions = Transaction.objects.filter(account_id=account_id)
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
