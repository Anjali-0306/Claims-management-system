from django.contrib import admin
from .models import Claim,ClaimStatusHistory

# Register your models here.
admin.site.register(Claim)
admin.site.register(ClaimStatusHistory)