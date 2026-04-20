"""
AISA Training Dataset — CLEAN Repo Serializers
aisa_label: clean
fix_applied: serializer_data_overexposure
notes: Explicit field lists only. No fields="__all__". 
       Read-only enforced on server-side fields.
"""

from rest_framework import serializers
from .models import Order, UserProfile


class OrderSerializer(serializers.ModelSerializer):
    """
    aisa_label: clean_serializer
    fix: Explicit fields listed — no PII, no sensitive data
    """
    class Meta:
        model = Order
        fields = ["id", "item", "amount", "status", "created_at"]
        read_only_fields = ["id", "status", "created_at"]  # ✅ status server-controlled


class OrderCreateSerializer(serializers.ModelSerializer):
    """
    aisa_label: clean_serializer
    fix: Separate write serializer — user set from request, not from input
    """
    class Meta:
        model = Order
        fields = ["item", "amount"]  # ✅ only what user should provide


class UserProfileSerializer(serializers.ModelSerializer):
    """
    aisa_label: clean_serializer
    fix: Only non-sensitive fields exposed (phone only)
    """
    class Meta:
        model = UserProfile
        fields = ["id", "phone"]  # ✅ no ssn, no token, no address
