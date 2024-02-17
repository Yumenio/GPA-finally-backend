import uuid
from django.db import models
from django.contrib.auth.models import User


class Account(models.Model):
    ID = models.AutoField(primary_key=True)
    account_id = models.CharField(max_length=10, unique=True)  # why two Id fields?
    account_number = models.CharField(max_length=16, unique=True)
    current_balance = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.account_id} - {self.account_number}"
