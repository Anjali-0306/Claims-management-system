from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
	class Role(models.TextChoices):
		CUSTOMER = "CUSTOMER","Customer"
		REVIEWER = "REVIEWER","Reviewer"

	role = models.CharField(max_length=20,choices=Role.choices)
	def is_customer(self):
		return self.role == self.Role.CUSTOMER

	def is_review(self):
		return self.role == self.Role.REVIEWER