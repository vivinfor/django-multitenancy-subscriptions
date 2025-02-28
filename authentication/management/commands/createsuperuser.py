from django.contrib.auth.management.commands.createsuperuser import Command as BaseCreateSuperuserCommand
from django.core.management import CommandError
from backend_services.subscriptions.subscriber_service import SubscriberService
from django.db import transaction


class Command(BaseCreateSuperuserCommand):
    """
    Comando customizado para criar superusuários, utilizando o SubscriberService.
    """

    def handle(self, *args, **options):
        # Coleta os argumentos do superusuário
        cpf = options.get("cpf")
        email = options.get("email")
        first_name = options.get("first_name", "Superuser")
        last_name = options.get("last_name", "Admin")
        password = options.get("password", None)

        # Valida campos obrigatórios
        if not cpf:
            raise CommandError("O campo CPF é obrigatório.")
        if not email:
            raise CommandError("O campo email é obrigatório.")
        if not password:
            raise CommandError("O campo senha é obrigatório para superusuários.")

        # Configuração do plano default (se necessário)
        default_plan = None  # Ajuste conforme a lógica de planos

        try:
            with transaction.atomic():
                # Usar o serviço para criar o tenant, usuário e assinante
                subscriber, user, tenant, _ = SubscriberService.create_subscriber_tenant_user(
                    cpf=cpf,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    plan=default_plan,
                    birth_date=None,  # Opcional, ajuste conforme necessário
                )

                # Atualizar permissões do superusuário
                user.is_staff = True
                user.is_superuser = True
                user.set_password(password)
                user.save()

                self.stdout.write(
                    self.style.SUCCESS(f"Superusuário e assinante criados com sucesso para CPF: {cpf}")
                )

        except Exception as e:
            raise CommandError(f"Erro ao criar superusuário ou assinante: {e}")
