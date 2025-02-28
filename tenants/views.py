from django.views.generic import ListView, DetailView, UpdateView
from django.urls import reverse_lazy
from tenants.models import Tenant, UserTenantAssociation

class TenantListView(ListView):
    model = Tenant
    template_name = 'flowbite/tenants/tenants_list.html'
    context_object_name = "tenants"
    
class TenantDetailView(DetailView):
    model = Tenant
    template_name = 'flowbite/tenants/tenant_detail.html'
    context_object_name = "tenant"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tenant = self.object
        context["associated_users"] = UserTenantAssociation.objects.filter(tenant=tenant).select_related("user")
        return context

class TenantUpdateView(UpdateView):
    model = Tenant
    fields = ["name", "is_active"]
    template_name = "admin/tenant_form.html"
    success_url = reverse_lazy("tenants:tenant_list")
