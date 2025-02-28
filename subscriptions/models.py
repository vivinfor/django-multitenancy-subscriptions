from django.db import models
from django.utils.translation import gettext_lazy as _
from tenants.models import Tenant

class Plan(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name=_("Nome"))
    price = models.PositiveIntegerField(default=0, verbose_name=_("Preço (R$)"))
    description = models.TextField(verbose_name=_("Descrição"), blank=True, null=True)
    is_active = models.BooleanField(default=True, verbose_name=_("Ativo"))
    user_limit = models.PositiveIntegerField(default=1, verbose_name=_("Quantidade de Usuários"))
    storage_limit_gb = models.PositiveIntegerField(default=1, verbose_name=_("Espaço de Armazenamento (GB)"))

    class Meta:
        verbose_name = _("Plano")
        verbose_name_plural = _("Planos")

    def __str__(self):
        return f"{self.name} - R$ {self.price}" 

class Subscriber(models.Model):
    cpf = models.CharField(max_length=11, verbose_name=_("CPF"))
    email = models.EmailField(unique=True, verbose_name=_("E-mail"))
    first_name = models.CharField(max_length=50, verbose_name=_("Nome"))
    last_name = models.CharField(max_length=50, verbose_name=_("Sobrenome"))
    signed_plan = models.ForeignKey(Plan, on_delete=models.PROTECT, verbose_name=_("Plano Assinado"))
    is_active = models.BooleanField(default=True, verbose_name=_("Está Ativo"))
    tenant = models.ForeignKey(Tenant, on_delete=models.PROTECT, related_name="subscribers", verbose_name=_("Tenant"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Criado Em"))
    
    class Meta:
        verbose_name = _( "Assinante")
        verbose_name_plural = _( "Assinantes")
        unique_together = [('tenant', 'cpf')]

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"
