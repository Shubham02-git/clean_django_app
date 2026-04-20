"""
AISA Training Dataset — CLEAN Repo Models
aisa_label: clean
expected_risk_score: < 10
notes: No sensitive fields exposed at model level.
       Proper field separation — PII kept internal.
"""

from django.db import models
from django.contrib.auth.models import User


class Order(models.Model):
    """
    aisa_label: clean_model
    notes: No raw PII stored. user FK enforced. status is server-controlled.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=50,
        default="pending",
        choices=[("pending", "Pending"), ("delivered", "Delivered"), ("cancelled", "Cancelled")]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order#{self.id} by {self.user}"


class UserProfile(models.Model):
    """
    aisa_label: clean_model
    notes: No SSN, no raw token stored. Phone is optional non-critical field.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"Profile of {self.user}"
