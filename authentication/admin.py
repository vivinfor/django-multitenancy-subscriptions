from django.contrib import admin
from authentication.models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("email", "first_name", "last_name", "cpf", "is_active", "is_staff", "tenant")
    list_filter = ("is_active", "is_staff", "tenant")
    search_fields = ("email", "first_name", "last_name", "cpf")
    ordering = ("email",)
    fieldsets = (
        ("Informações Pessoais", {"fields": ("first_name", "last_name", "email", "cpf", "tenant")}),
        ("Permissões", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Datas Importantes", {"fields": ("last_login", "date_joined")}),
    )
    filter_horizontal = ("groups", "user_permissions")
