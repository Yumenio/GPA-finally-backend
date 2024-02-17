from ninja import Router

from api.schemas.transaction import TransactionCreateSchema, TransactionUpdateSchema

router = Router()


@router.post("create/")
def create_transaction(request, transaction: TransactionCreateSchema):
    return {"created": transaction.model_dump()}


@router.get("{id}")
def get_transaction(request, id):
    return {"transaction_id": id}


@router.get("")
def get_all_transactions(request):
    return {"all_transactions": []}


@router.put("{id}")
def update_transaction(request, id, transactionData: TransactionUpdateSchema):
    return {"updated": transactionData.model_dump()}


@router.delete("{id}")
def delete_transaction(request, id):
    return {"deleted": id}
