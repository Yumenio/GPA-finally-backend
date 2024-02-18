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

    def save(self, *args, **kwargs):
        if not self.account_id:
            latest_account = Account.objects.order_by("-ID").first()
            if latest_account and latest_account.account_id:
                last_id = int(latest_account.account_id.split("-")[1])
                self.account_id = "A-{0:04d}".format(last_id + 1)
            else:
                self.account_id = "A-0001"

        if not self.account_number:
            # Generate account_number if not provided
            latest_account = Account.objects.order_by("-ID").first()
            if latest_account and latest_account.account_number:
                last_number = int(latest_account.account_number.replace(" ", ""))
                self.account_number = "{:016d}".format(last_number + 1)
            else:
                self.account_number = "0000000000000001"

        super(Account, self).save(*args, **kwargs)
