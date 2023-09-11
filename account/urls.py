from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.AuthenticationView.as_view(), name='login'),
]
