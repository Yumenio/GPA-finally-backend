from enum import Enum
from ninja import ModelSchema
from api.models.transaction import Transaction


class TransactionTypes(Enum):
    credit = "CREDIT"
    debit = "DEBIT"


class TransactionSchema(ModelSchema):
    class Meta:
        model = Transaction
        exclude = ["ID", "account"]

    transaction_type: TransactionTypes


class TransactionCreateSchema(TransactionSchema):
    account_id: int


class TransactionUpdateSchema(TransactionSchema):
    pass
