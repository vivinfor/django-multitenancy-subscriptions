from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from .models import Tenant, Plan
from .forms import AdminUserCreationForm, RegularUserCreationForm

class UserCreationTests(TestCase):
    
    def setUp(self):
        # Criar um plano com limite de usuários
        self.plan = Plan.objects.create(name='Plano Básico', max_users=10)

        # Criar um tenant associado ao plano
        self.tenant = Tenant.objects.create(name='Tenant 1', plan=self.plan)

        # Criar um usuário administrativo
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@tenant1.com',
            password='admin123',
            tenant=self.tenant
        )

    def test_create_regular_user(self):
        """Teste para criação de um usuário regular."""
        user_data = {
            'cpf': '12345678901',
            'email': 'user@tenant1.com',
            'first_name': 'João',
            'last_name': 'Silva',
            'password1': 'senha123',
            'password2': 'senha123',
        }
        form = RegularUserCreationForm(data=user_data)
        self.assertTrue(form.is_valid())

        # Salvar o usuário
        user = form.save(commit=False)
        user.set_password(user_data['password1'])
        user.tenant = self.tenant
        user.save()

        # Verificar se o usuário foi salvo no banco de dados
        self.assertEqual(get_user_model().objects.count(), 2)  # 1 admin + 1 regular

    def test_check_plan_limits_for_users(self):
        """Teste para verificar se o limite de usuários do plano é respeitado."""
        # Criar usuários até o limite do plano
        for i in range(10):  # Max users = 10
            user_data = {
                'cpf': f'1234567890{i}',
                'email': f'user{i}@tenant1.com',
                'first_name': f'User{i}',
                'last_name': f'Last{i}',
                'password1': 'senha123',
                'password2': 'senha123',
            }
            form = RegularUserCreationForm(data=user_data)
            form.is_valid()
            user = form.save(commit=False)
            user.set_password(user_data['password1'])
            user.tenant = self.tenant
            user.save()

        # Tentar criar mais um usuário além do limite
        user_data = {
            'cpf': '123456789012',
            'email': 'user11@tenant1.com',
            'first_name': 'User11',
            'last_name': 'Last11',
            'password1': 'senha123',
            'password2': 'senha123',
        }
        form = RegularUserCreationForm(data=user_data)
        with self.assertRaises(ValidationError):
            form.is_valid()
            form.save()

    def test_admin_creation_form(self):
        """Teste para o formulário de criação de administradores."""
        user_data = {
            'first_name': 'Admin',
            'last_name': 'User',
            'email': 'admin@tenant1.com',
            'password': 'admin123',
            'is_staff': True,
            'is_active': True,
            'tenant': self.tenant,
        }
        form = AdminUserCreationForm(data=user_data)
        self.assertTrue(form.is_valid())

        # Salvar o usuário administrativo
        admin_user = form.save(commit=False)
        admin_user.set_password(user_data['password'])
        admin_user.save()

        # Verificar se o usuário foi salvo corretamente
        self.assertEqual(get_user_model().objects.count(), 2)  # 1 admin + 1 regular


class PlanServiceTest(TestCase):
    
    def setUp(self):
        plan = Plan.objects.create(name="Plano Básico", max_users=10)
        tenant = Tenant.objects.create(name="Tenant 1", plan=plan)
        self.tenant = tenant
        
        # Criar usuários
        for i in range(10):
            CustomUser.objects.create(tenant=tenant, email=f"user{i}@example.com")
    
    def test_check_plan_limits_success(self):
        # Quando o número de usuários for menor que o limite
        tenant = self.tenant
        tenant.users.all().delete()  # Limpar usuários
        CustomUser.objects.create(tenant=tenant, email="user11@example.com")
        
        # Verifique se não há exceções quando o limite de usuários não for atingido
        try:
            PlanService.check_plan_limits(tenant)
        except ValidationError:
            self.fail("check_plan_limits não deveria ter levantado uma exceção.")
    
    def test_check_plan_limits_error(self):
        # Quando o número de usuários atingir o limite
        tenant = self.tenant
        
        # Verifique se a exceção de limite é levantada
        with self.assertRaises(ValidationError):
            PlanService.check_plan_limits(tenant)
