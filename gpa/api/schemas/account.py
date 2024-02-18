from ninja import ModelSchema
from api.models.account import Account


class AccountSchema(ModelSchema):
    class Meta:
        model = Account
        fields = ["current_balance"]
        optional_fields = ["current_balance"]


class AccountCreateSchema(AccountSchema):
    user_id: int


class AccountUpdateSchema(AccountSchema):
    pass
