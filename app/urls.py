from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from django.shortcuts import render

urlpatterns = [
    # Rotas de administração
    path('admin/', admin.site.urls),
    
    # Rota raiz redireciona para a home
    path('', lambda request: render(request, 'flowbite/index.html'), name='home'),
    # Apps
    path('authentication/', include(('authentication.urls', 'authentication'), namespace='authentication')),
    path('subscriptions/', include(('subscriptions.urls', 'subscriptions'), namespace='subscriptions')),
    path('tenants/', include(('tenants.urls', 'tenants'), namespace='tenants')),
]

# Servir arquivos estáticos no modo DEBUG
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

