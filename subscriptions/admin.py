from django.contrib import admin
from .models import Plan, Subscriber

@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    """
    Configuração do Django Admin para o modelo Plan.
    """
    list_display = (
        'name',
        'price',
        'user_limit',
        'storage_limit_gb',
        'is_active',
    )
    list_filter = ('is_active',)  # Filtro lateral para status
    search_fields = ('name', 'description')  # Campos pesquisáveis
    ordering = ('price',)  # Ordenação padrão pelo preço

    fieldsets = (
        (None, {
            'fields': ('name', 'price', 'description')
        }),
        ('Recursos', {
            'fields': ('user_limit', 'storage_limit_gb')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )

@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    """
    Configuração do Django Admin para o modelo Subscriber.
    """
    list_display = (
        'first_name',
        'last_name',
        'email',
        'cpf',
        'signed_plan',
        'tenant',
        'is_active',
        'created_at',
    )
    list_filter = ('signed_plan', 'tenant', 'is_active')  # Filtro lateral
    search_fields = ('first_name', 'last_name', 'email', 'cpf')  # Campos pesquisáveis
    ordering = ('created_at',)  # Ordenação padrão por data de criação
    date_hierarchy = 'created_at'  # Navegação por datas

    fieldsets = (
        ('Informações Pessoais', {
            'fields': ('first_name', 'last_name', 'cpf', 'email')
        }),
        ('Plano', {
            'fields': ('signed_plan', 'tenant')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )
