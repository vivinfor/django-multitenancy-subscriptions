from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.exceptions import ValidationError

class CustomUserManager(BaseUserManager):
    def create_user(self, cpf, email, password=None, tenant=None, **extra_fields):
        """
        Cria e retorna um usuário normal.
        """
        if not cpf or not email or not tenant:
            raise ValueError("CPF, Email e Tenant são obrigatórios.")
        email = self.normalize_email(email)
        user = self.model(cpf=cpf, email=email, tenant=tenant, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, cpf, email, password=None, **extra_fields):
        """
        Cria e retorna um superusuário, garantindo que tenha um tenant atribuído.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if not password:
            raise ValueError("Superusuários precisam de uma senha.")

        from django.apps import apps
        Tenant = apps.get_model("tenants", "Tenant")

        tenant = Tenant.objects.first()
        if not tenant:
            tenant = Tenant.objects.create(name="AdminTenant")

        extra_fields["tenant"] = tenant

        return self.create_user(cpf, email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    tenant = models.ForeignKey('tenants.Tenant', on_delete=models.CASCADE, related_name="custom_users")
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    cpf = models.CharField(max_length=11, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'cpf'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"

    def save(self, *args, **kwargs):
        if not self.tenant:
            raise ValidationError("Todos os usuários precisam estar associados a um Tenant.")
        super().save(*args, **kwargs)
