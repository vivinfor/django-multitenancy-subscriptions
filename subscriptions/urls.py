from django.urls import path
from django.views.generic import ListView, DetailView, UpdateView
from subscriptions.models import Plan, Subscriber

app_name = "subscriptions"

class PlanListView(ListView):
    model = Plan
    template_name = 'subscriptions/plan_list.html'
    context_object_name = "plans"

class PlanUpdateView(UpdateView):
    model = Plan
    fields = ["name", "price", "user_limit", "storage_limit_gb", "is_active"]
    template_name = "subscriptions/plan_form.html"
    success_url = "/subscriptions/plans/"

class SubscriberListView(ListView):
    model = Subscriber
    template_name = 'subscriptions/subscriber_list.html'
    context_object_name = "subscribers"

class SubscriberDetailView(DetailView):
    model = Subscriber
    template_name = 'subscriptions/subscriber_detail.html'
    context_object_name = "subscriber"

urlpatterns = [
    path("plans/", PlanListView.as_view(), name="plan_list"),
    path("plans/update/<int:pk>/", PlanUpdateView.as_view(), name="plan_update"),
    path("subscribers/", SubscriberListView.as_view(), name="subscriber_list"),
    path("subscribers/<int:pk>/", SubscriberDetailView.as_view(), name="subscriber_detail"),
]
