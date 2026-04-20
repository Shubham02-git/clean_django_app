"""
AISA Training Dataset — CLEAN Repo URLs
aisa_label: clean
notes: All endpoints require authentication. No public data dumps.
"""

from django.urls import path
from api.views import (
    OrderDetailView,
    OrderListView,
    OrderCreateView,
    UserProfileView,
    AdminUserListView,
    TokenInfoView,
)

urlpatterns = [
    # ✅ Object-level auth enforced
    path("api/orders/<int:id>/", OrderDetailView.as_view(), name="order-detail"),

    # ✅ Scoped to request.user only
    path("api/orders/", OrderListView.as_view(), name="order-list"),

    # ✅ Mass assignment protected
    path("api/orders/create/", OrderCreateView.as_view(), name="order-create"),

    # ✅ Only safe fields returned
    path("api/profile/", UserProfileView.as_view(), name="user-profile"),

    # ✅ IsAdminUser guard
    path("api/admin/users/", AdminUserListView.as_view(), name="admin-users"),

    # ✅ No token reflection
    path("api/token/info/", TokenInfoView.as_view(), name="token-info"),
]
