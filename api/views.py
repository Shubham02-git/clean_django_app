"""
AISA Training Dataset — CLEAN Repo Views
aisa_label: clean
expected_risk_score: < 10

All vulnerabilities from vuln_django_app have been fixed here.
Each view documents WHAT was fixed and WHY.
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import TokenAuthentication
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

from .models import Order, UserProfile
from .serializers import (
    OrderSerializer,
    OrderCreateSerializer,
    UserProfileSerializer,
)


# ─────────────────────────────────────────────
# FIX #1: IDOR → Object-Level Auth enforced
# was: Order.objects.get(id=id)
# now: filter by BOTH id AND request.user
# ─────────────────────────────────────────────
class OrderDetailView(APIView):
    """
    aisa_label: clean
    fix_applied: missing_object_level_auth
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]          # ✅ must be logged in

    def get(self, request, id):
        # ✅ filter(user=request.user) prevents IDOR — user can only see own orders
        order = get_object_or_404(Order, id=id, user=request.user)
        serializer = OrderSerializer(order)
        return Response(serializer.data)


# ─────────────────────────────────────────────
# FIX #2: Missing Auth → IsAuthenticated enforced
# was: no permission_classes, Order.objects.all()
# now: scoped to request.user only
# ─────────────────────────────────────────────
class OrderListView(APIView):
    """
    aisa_label: clean
    fix_applied: missing_authentication, unsafe_queryset_filtering
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]          # ✅ must be logged in

    def get(self, request):
        # ✅ always scoped to the requesting user — no user_id param accepted
        orders = Order.objects.filter(user=request.user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)


# ─────────────────────────────────────────────
# FIX #3: Mass Assignment → separate write serializer
# was: OrderSerializer(data=request.data) — all fields writable
# now: OrderCreateSerializer only accepts item + amount
# ─────────────────────────────────────────────
class OrderCreateView(APIView):
    """
    aisa_label: clean
    fix_applied: mass_assignment
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = OrderCreateSerializer(data=request.data)
        if serializer.is_valid():
            # ✅ user is set from request.user — not from POST body
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ─────────────────────────────────────────────
# FIX #4: Serializer overexposure → explicit fields
# was: UserProfileSerializer(fields="__all__") → ssn, token exposed
# now: only phone field returned
# ─────────────────────────────────────────────
class UserProfileView(APIView):
    """
    aisa_label: clean
    fix_applied: serializer_data_overexposure
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # ✅ scoped to own profile, explicit safe fields only
        profile = get_object_or_404(UserProfile, user=request.user)
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data)


# ─────────────────────────────────────────────
# FIX #5: Admin endpoint → IsAdminUser guard
# was: no permission check, User.objects.all()
# now: IsAdminUser required, limited fields returned
# ─────────────────────────────────────────────
class AdminUserListView(APIView):
    """
    aisa_label: clean
    fix_applied: admin_endpoint_no_permission_check
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]              # ✅ staff only

    def get(self, request):
        # ✅ limited fields — no password hash, no sensitive flags leaked
        users = User.objects.values("id", "username", "email", "date_joined")
        return Response(list(users))


# ─────────────────────────────────────────────
# FIX #6: Token reflection → no echo, server-side validation only
# was: return Response({"token": token})
# now: validates token, returns only safe user info
# ─────────────────────────────────────────────
class TokenInfoView(APIView):
    """
    aisa_label: clean
    fix_applied: token_reflection_no_validation
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # ✅ token is validated by TokenAuthentication before reaching here
        # ✅ we never echo the token back — only return safe user info
        return Response({
            "user": request.user.username,
            "is_staff": request.user.is_staff,
        })
