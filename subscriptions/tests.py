from django.test import TestCase
from django.urls import reverse

class SubscriptionTests(TestCase):

    def test_homepage_loads(self):
        """Verifica se a página inicial carrega corretamente"""
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

    def test_subscription_list_view(self):
        """Verifica se a rota de assinaturas retorna 200"""
        response = self.client.get(reverse("subscriptions:subscription_list"))
        self.assertEqual(response.status_code, 200)

    def test_invalid_url_returns_404(self):
        """Verifica se uma URL inválida retorna erro 404"""
        response = self.client.get("/invalid-url/")
        self.assertEqual(response.status_code, 404)
