from django.core.exceptions import PermissionDenied

class GlobalPermissionMixin:
    def dispatch(self, request, *args, **kwargs):
        """
        Verifica as permissões antes de permitir o acesso à view.
        """
        if not self.has_permission(request):
            raise PermissionDenied("Você não tem permissão para acessar esta página.")
        return super().dispatch(request, *args, **kwargs)

    def has_permission(self, request):
        """
        Adapta a lógica do `GlobalDefaultPermission` para o contexto de templates.
        """
        model_permission_codename = self.get_model_permission_codename(request)

        if not model_permission_codename:
            return False

        return request.user.has_perm(model_permission_codename)

    def get_model_permission_codename(self, request):
        """
        Gera o codename da permissão com base no método HTTP e no modelo associado à view.
        """
        try:
            model_name = self.get_queryset().model._meta.model_name
            app_label = self.get_queryset().model._meta.app_label
            action = self.get_action_suffix(request.method)
            return f"{app_label}.{action}_{model_name}"
        except AttributeError:
            return None

    @staticmethod
    def get_action_suffix(method):
        """
        Mapeia os métodos HTTP para ações de permissão.
        """
        method_actions = {
            'GET': 'view',
            'POST': 'add',
            'PUT': 'change',
            'PATCH': 'change',
            'DELETE': 'delete',
        }
        return method_actions.get(method, '')
