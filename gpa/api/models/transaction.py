from django.db import models
from api.models.account import Account


class Transaction(models.Model):
    TRANSACTION_TYPES = (("CREDIT", "Credit"), ("DEBIT", "Debit"))

    ID = models.AutoField(primary_key=True)
    date = models.DateField()
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    note = models.TextField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.transaction_type} - {self.amount}"
