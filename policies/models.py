from django.db import models
from django.conf import settings
User = settings.AUTH_USER_MODEL
class Policy(models.Model):
	class Status(models.TextChoices):
		ACTIVE = "ACTIVE","Active"
		INACTIVE = "INACTIVE","Inactive"

	policy_number = models.CharField(max_length=50, unique=True)
	customer = models.ForeignKey(User,on_delete=models.PROTECT,related_name="policies")
	status = models.CharField(max_length=20,choices=Status.choices,default=Status.ACTIVE)
	created_at = models.DateTimeField(auto_now_add=True)
	def is_active(self):
		return self.status == self.Status.ACTIVE


	def __str__(self):
		return self.policy_number
