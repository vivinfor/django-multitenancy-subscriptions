from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages

@method_decorator(csrf_exempt, name='dispatch')
class CustomLoginView(LoginView):
    """
    View de login customizada.
    """
    template_name = 'flowbite/pages/login.html'
    redirect_authenticated_user = True
    success_url = reverse_lazy("home")

class CustomLogoutView(LogoutView):
    """
    View de logout customizada.
    """
    def dispatch(self, request, *args, **kwargs):
        logout(request)
        request.session.flush()
        return redirect(reverse_lazy("authentication:login"))

