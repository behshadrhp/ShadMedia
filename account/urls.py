from django.urls import path
from django.contrib.auth import views as auth_view

from . import views


urlpatterns = [
    # home page
    path('', views.HomeView.as_view(), name='home'),
    # dashboard
    path('account/dashboard/', views.DashboardView.as_view(), name='dashboard'),
    # authentication page
    path('account/register/', views.RegisterView.as_view(), name='register'),
    path('account/login/', views.LoginView.as_view(), name='login'),
    path('account/logout/', views.LogoutView.as_view(), name='logout'),
    # change password
    path('account/password-change/', views.PasswordChangeView.as_view(), name='password_change'),
]
