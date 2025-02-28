from django.urls import path
from .views import TenantListView, TenantDetailView, TenantUpdateView

app_name = 'tenants'

urlpatterns = [
    path("", TenantListView.as_view(), name="tenant_list"),
    path("<int:pk>/", TenantDetailView.as_view(), name="tenant_detail"),
    path("<int:pk>/update/", TenantUpdateView.as_view(), name="tenant_update"),
]
