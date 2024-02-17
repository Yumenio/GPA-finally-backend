from ninja import Router
from schemas.account import AccountSchema, AccountCreateSchema, AccountUpdateSchema

router = Router()


@router.post("create")
def create_account(request, account: AccountCreateSchema):
    return {"status": "account created succesfully"}


@router.get("{id}")
def get_account(request, id):
    return {"account_id": id}


@router.get("")
def get_all_accounts(request):
    return {"all_accounts": []}


@router.put("{id}")
def update_account(request, id, accountData: AccountUpdateSchema):
    return {"updated_account_id": id}


@router.delete("{id}")
def delete_account(request, id):
    return {"deteled_account_id": id}
