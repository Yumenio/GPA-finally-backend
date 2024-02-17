from ninja import ModelSchema
from api.models.transaction import Transaction


class TransactionSchema(ModelSchema):
    class Meta:
        model = Transaction
        exclude = ["ID"]


class TransactionCreateSchema(TransactionSchema):
    pass


class TransactionUpdateSchema(TransactionSchema):
    pass
