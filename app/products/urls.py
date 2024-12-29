from django.urls import path
from products.views import ProductAlertsAPIView, ProductsAPIView, ProductsByAlertStatusAPIView, ProductsByDateAPIView, ProductsByDaysAPIView

urlpatterns = [
    path('', ProductsAPIView.as_view(), name='products'),
    path('<int:pk>/', ProductsAPIView.as_view(), name='product-detail'),
    path('<int:pk>/alerts/', ProductAlertsAPIView.as_view(), name='product-alerts'),
    path('filter-by-dates/', ProductsByDateAPIView.as_view(), name='products-by-dates'),
    path('filter-by-days/', ProductsByDaysAPIView.as_view(), name='products-by-days'),
    path('filter-by-alert-status/', ProductsByAlertStatusAPIView.as_view(), name='products-by-alert-status'),
]

