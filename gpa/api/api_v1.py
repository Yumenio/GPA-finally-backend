from ninja import NinjaAPI
from django.conf import settings
from api.accounts.accounts import router as account_router

api = NinjaAPI(title=settings.APP_NAME, csrf=False, version="1.0")

api.add_router("accounts", account_router)
