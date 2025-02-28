from django.contrib import admin
from django.urls import path
from tenants.models import Tenant, TenantDomain, UserTenantAssociation
from tenants.views import TenantListView, TenantDetailView, TenantUpdateView

@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active", "created_at")
    search_fields = ("name",)
    list_filter = ("is_active",)
    ordering = ("name",)

@admin.register(TenantDomain)
class TenantDomainAdmin(admin.ModelAdmin):
    list_display = ("tenant", "domain", "is_primary")
    search_fields = ("domain",)
    list_filter = ("is_primary",)

@admin.register(UserTenantAssociation)
class UserTenantAssociationAdmin(admin.ModelAdmin):
    list_display = ("user", "tenant", "role", "created_at")
    search_fields = ("user__email", "tenant__name")
    list_filter = ("role",)

