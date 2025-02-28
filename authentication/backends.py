import logging
from django.contrib.auth.backends import ModelBackend
from authentication.models import CustomUser

logger = logging.getLogger(__name__)

class TenantAwareBackend(ModelBackend):
    """
    Backend de autenticação baseado no CPF, garantindo que o usuário pertence a um tenant ativo.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        if not username or not password:
            return None

        # Busca usuário pelo CPF sem gerar exceção
        user = CustomUser.objects.filter(cpf=username).first()
        if not user:
            return None

        # Verifica se o usuário pertence a um tenant ativo
        if not user.tenant or not user.tenant.is_active:
            logger.warning(f"Tentativa de login negada: Usuário '{username}' sem tenant ativo.")
            return None

        # Verifica a senha e autentica
        if user.check_password(password) and self.user_can_authenticate(user):
            if request is not None:
                request.tenant = user.tenant  # Define o tenant no request
            return user
        
        logger.warning(f"Tentativa de login falha para o CPF: {username}")
        return None
