from django.db import models
from django.utils.translation import gettext_lazy as _
from simple_history.models import HistoricalRecords
from authentication.models import CustomUser

class Tenant(models.Model):
    """
    Representa uma unidade de organização (empresa ou grupo) que utiliza o sistema.
    """
    history = HistoricalRecords()
    name = models.CharField(max_length=150, unique=True, verbose_name=_("Name"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))
    is_active = models.BooleanField(default=True, verbose_name=_("Is Active"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Tenant"
        verbose_name_plural = "Tenants"

class TenantDomain(models.Model):
    """
    Gerencia o domínio associado a um tenant.
    """
    tenant = models.OneToOneField(
        Tenant,
        on_delete=models.CASCADE,
        related_name="domain",
        verbose_name=_("Tenant")
    )
    domain = models.CharField(max_length=253, unique=True, verbose_name=_("Domain"))
    is_primary = models.BooleanField(default=True, verbose_name=_("Is Primary"))

    def __str__(self):
        return self.domain

class UserTenantAssociation(models.Model):
    """
    Relaciona usuários a tenants com permissões associadas.
    """
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="tenants")
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="users")
    role = models.CharField(max_length=50, choices=[("admin", "Admin"), ("user", "User")], default="user")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "tenant")

    def __str__(self):
        return f"{self.user.email} -> {self.tenant.name}"

