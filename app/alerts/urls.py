from django.urls import path

from alerts.views import AlertsAPIView, AlertsByStatusAPIView



urlpatterns = [
    path('', AlertsAPIView.as_view(), name='alerts'),
    path('<int:pk>/', AlertsAPIView.as_view(), name='alert-detail'),
    path('filter-by-status/', AlertsByStatusAPIView.as_view(), name='alerts-filter-by-status'),
]