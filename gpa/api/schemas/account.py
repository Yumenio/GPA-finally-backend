from ninja import ModelSchema
from api.models.account import Account


class AccountSchema(ModelSchema):
    user_id: int

    class Meta:
        model = Account
        fields = ["current_balance"]
        optional_fields = ["current_balance"]


class AccountCreateSchema(AccountSchema):
    pass


class AccountUpdateSchema(AccountSchema):
    pass
