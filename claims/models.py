from django.db import models
from django.conf import settings
from policies.models import Policy
from .exceptions import InvalidClaimState

User = settings.AUTH_USER_MODEL

# Assuming InvalidClaimState is defined elsewhere or imported
class InvalidClaimState(Exception):
    pass

class Claim(models.Model):
    class Status(models.TextChoices):
        DRAFT = "DRAFT", "Draft"
        SUBMITTED = "SUBMITTED", "Submitted"
        APPROVED = "APPROVED", 'Approved'
        REJECTED = "REJECTED", "Rejected"

    policy = models.ForeignKey(Policy, on_delete=models.PROTECT, related_name="claims")
    customer = models.ForeignKey(User, on_delete=models.PROTECT, related_name="claims")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    ALLOWED_TRANSITIONS = {
        Status.DRAFT: {Status.SUBMITTED},
        Status.SUBMITTED: {Status.APPROVED, Status.REJECTED},
    }

    def update_draft(self, **data):
        """Updates fields only if the claim is still in DRAFT status."""
        if self.status != self.Status.DRAFT:
            raise InvalidClaimState("Only draft claims can be updated!")

        for field, value in data.items():
            setattr(self, field, value)

        self.save(update_fields=data.keys())

    def submit(self, user):
        """Moves claim from DRAFT to SUBMITTED and logs history."""
        if self.status != self.Status.DRAFT:
            raise InvalidClaimState("Only draft claims can be submitted!")

        previous_status = self.status
        self.status = self.Status.SUBMITTED
        self.save(update_fields=['status'])

        # Create audit trail entry
        ClaimStatusHistory.objects.create(
            claim=self,
            previous_status=previous_status,
            new_status=self.Status.SUBMITTED,
            changed_by=user,
        )

    def approve(self, reviewer):
        """Moves claim from SUBMITTED to APPROVED and logs history."""
        if self.status != self.Status.SUBMITTED:
            raise InvalidClaimState("Only Submitted claims can be approved!")

        previous_status = self.status
        self.status = self.Status.APPROVED
        self.save(update_fields=['status'])

        ClaimStatusHistory.objects.create(
            claim=self,
            previous_status=previous_status,
            new_status=self.Status.APPROVED,
            changed_by=reviewer,
        )

    def reject(self, reviewer):
        """Moves claim from SUBMITTED to REJECTED and logs history."""
        if self.status != self.Status.SUBMITTED:
            raise InvalidClaimState("Only Submitted claims can be rejected!")

        previous_status = self.status
        self.status = self.Status.REJECTED
        self.save(update_fields=['status'])

        ClaimStatusHistory.objects.create(
            claim=self,
            previous_status=previous_status,
            new_status=self.Status.REJECTED,
            changed_by=reviewer,
        )

class ClaimStatusHistory(models.Model):
    claim = models.ForeignKey(Claim, on_delete=models.CASCADE, related_name="status_history")
    previous_status = models.CharField(max_length=20)
    new_status = models.CharField(max_length=20)
    changed_by = models.ForeignKey(User, on_delete=models.PROTECT)
    changed_at = models.DateTimeField(auto_now_add=True)