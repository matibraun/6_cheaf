from django.urls import path
from .views import CustomLoginView, RegisterUserView

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
]