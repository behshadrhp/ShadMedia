from django.urls import path

from . import views


urlpatterns = [
    # home page
    path('', views.HomeView.as_view(), name='home'),
    # authentication page
    path('account/login/', views.AuthenticationView.as_view(), name='login'),
    path('account/logout/', views.LogoutView.as_view(), name='logout'),
]
