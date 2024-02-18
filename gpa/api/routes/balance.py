from ninja import Router
from datetime import date
from django.shortcuts import get_object_or_404

from api.models.account import Account
from api.models.transaction import Transaction

router = Router()


@router.get("{account_id}")
def get_balance_at_day(request, account_id, date: date):
    account = get_object_or_404(Account, ID=account_id)
    transactions = Transaction.objects.filter(date__lte=date, account_id=account.ID)
    balance = 0
    balance += sum(
        [t.amount if t.transaction_type == "DEBIT" else -t.amount for t in transactions]
    )
    return {"balance": balance}
