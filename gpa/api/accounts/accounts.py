from ninja import Router

router = Router()


@router.post("create/")
def create_account(request):
    return {"status": "account created succesfully"}
