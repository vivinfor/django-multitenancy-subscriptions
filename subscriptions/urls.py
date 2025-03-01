from django.urls import path
from django.views.generic import ListView, DetailView, UpdateView

from subscriptions.views import PlanListView, PlanUpdateView, SubscriberDetailView, SubscriberListView

app_name = "subscriptions"

urlpatterns = [
    path("plans/", PlanListView.as_view(), name="plan_list"),
    path("plans/update/<int:pk>/", PlanUpdateView.as_view(), name="plan_update"),
    path("subscribers/", SubscriberListView.as_view(), name="subscriber_list"),
    path("subscribers/<int:pk>/", SubscriberDetailView.as_view(), name="subscriber_detail"),
]
