import pytz
import datetime

from django.db import models
from django.utils.timezone import now
from api.models import SatsUser

class WithdrawalRequests(models.Model):
	expiry = models.BigIntegerField()
	min_withdrawable = models.IntegerField()
	max_withdrawable = models.IntegerField()
	amount_withdrawn = models.IntegerField(null=True)
	user = models.ForeignKey(SatsUser, on_delete=models.CASCADE)
	funds_claimed = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"ID: {self.pk} - expiry: {self.expiry}  - max_withdrawable: {self.max_withdrawable}  - min_withdrawable: {self.min_withdrawable} - amount_withdrawn: {self.amount_withdrawn} - user: {self.user} - funds_claimed: {self.funds_claimed} - created_at: {self.created_at}"
