from django.contrib import admin
from subscriptions.models import Plan, Subscriber

@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    """
    Configuração do Django Admin para o modelo Plan.
    """
    list_display = (
        'name',
        'price',
        'is_active',
        'is_internal',
        'tenants_count',
    )
    list_filter = ('is_active', 'is_internal')  # Filtros laterais para status e uso interno
    search_fields = ('name', 'description')  # Campos pesquisáveis
    ordering = ('name',)  # Ordenação padrão por nome
    readonly_fields = ('tenants_count',)  # Campo somente leitura no admin

    fieldsets = (
        (None, {
            'fields': ('name', 'price', 'description', 'features', 'limits')
        }),
        ('Limites', {
            'fields': ('max_users',)
        }),
        ('Status', {
            'fields': ('is_active', 'is_internal')
        }),
    )

    def tenants_count(self, obj):
        """
        Retorna o número de tenants associados ao plano.
        """
        return obj.tenants_count
    tenants_count.short_description = "Tenants Count"  # Rótulo para o campo no admin


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    """
    Configuração do Django Admin para o modelo Subscriber.
    """
    list_display = (
        'first_name',
        'last_name',
        'email',
        'phone',
        'signed_plan',
        'tenant',
        'is_active',
        'created_at',
    )
    list_filter = ('signed_plan', 'tenant', 'is_active')  # Agora filtra também por is_active
    search_fields = ('first_name', 'last_name', 'email', 'phone', 'cpf')  # Incluído phone e cpf
    ordering = ('created_at',)  # Ordenação padrão por data de criação
