from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from django.shortcuts import render
from django.db import IntegrityError
from django.urls import resolve

class TenantContextMiddleware:
    """
    Middleware para injetar o tenant no request com base no usuário autenticado.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.tenant = getattr(request.user, 'tenant', None) if getattr(request, 'user', None) and request.user.is_authenticated else None
        return self.get_response(request)


class TenantAppMiddleware(MiddlewareMixin):
    """
    Middleware para carregar dinamicamente os apps ativos no tenant.
    """
    def process_request(self, request):
        try:
            from tenants.models import App  # Certifique-se de que o modelo existe e está correto
            if not getattr(settings, 'TENANT_APPS_LOADED', False):
                active_apps = list(App.objects.filter(is_active=True).values_list('name', flat=True))
                settings.INSTALLED_APPS += tuple(active_apps)
                settings.TENANT_APPS_LOADED = True
        except ImportError:
            pass  # Modelo `App` não encontrado; continue normalmente
        except Exception as e:
            print(f"Erro ao carregar os aplicativos do tenant: {e}")


class ErrorHandlingMiddleware:
    """
    Middleware para capturar erros comuns e exibir uma página genérica de erro.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            return self.get_response(request)
        except IntegrityError:
            return render(request, "errors/generic_error.html", {"error_message": "Houve um problema ao processar sua solicitação."}, status=400)
        except Exception as e:
            print(f"Erro não tratado: {e}")
            return render(request, "errors/generic_error.html", {"error_message": "Algo deu errado. Tente novamente mais tarde."}, status=500)


class LastListViewMiddleware:
    """
    Middleware para armazenar a última URL de listagem acessada pelo usuário.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.method == 'GET':
            current_url_name = resolve(request.path_info).url_name
            if current_url_name and 'list' in current_url_name:
                request.session['last_list_url'] = request.path_info
        return response

