from django.urls import path
from django.contrib.auth import views as auth_views

from . import views


urlpatterns = [
    # home page
    path('', views.HomeView.as_view(), name='home'),
    # dashboard page
    path('account/dashboard/', views.DashboardView.as_view(), name='dashboard'),
    # profile page
    path('account/profile/', views.ProfileView.as_view(), name='profile'),
    # authentication page
    path('account/register/', views.RegisterView.as_view(), name='register'),
    path('account/login/', views.LoginView.as_view(), name='login'),
    path('account/logout/', views.LogoutView.as_view(), name='logout'),
    # listing users and review detail information users
    path('account/users/', views.UserListView.as_view(), name='user_list'),
    path('account/users/<username>/', views.UserDetailView.as_view(), name='user_detail'),
    path('account/follow/', views.UserFollowView.as_view(), name='user_follow'),
    # change password
    path('account/password-change/', views.PasswordChangeView.as_view(), name='password_change'),
    # reset password
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name = 'account/password-reset/reset_password.html'), name ='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name = 'account/password-reset/password_reset_sent.html'), name ='password_reset_done'),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name = 'account/password-reset/password_reset_form.html'), name ='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name = 'account/password-reset/password_reset_done.html'), name ='password_reset_complete')
]
