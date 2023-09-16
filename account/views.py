from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required

from .forms import LoginForm, RegisterForm, ProfileForm


class HomeView(View):
    '''This class is for return home page.'''

    def get(self, request):
        context = {}
        return render(request, 'home.html', context)


class DashboardView(View):
    '''This class is for Dashboard panel.'''

    def get(self, request):
        if request.user.is_authenticated:
            context = {'section': 'dashboard'}
            return render(request, 'account/dashboard.html', context)
        else:
            return redirect('login')


class ProfileView(View):
    '''This class is for update profile account.'''

    def get(self, request):
        form = ProfileForm(instance=request.user.profile)

        context = {'form': form}
        return render(request, 'account/profile.html', context)

    def post(self, request):
        form = ProfileForm(request.POST)

        if form.is_valid():
            # dont save -> apply change
            profile = form.save(commit=False)
            # apply change avatar
            profile = request.user.profile
            profile.avatar = form.cleaned_data['avatar']
            profile.first_name = form.cleaned_data['first_name']
            profile.last_name = form.cleaned_data['last_name']
            profile.birthday = form.cleaned_data['birthday']
            # save user
            profile.save()
            messages.success(request, 'Your profile has been updated')
        else:
            messages.error(request, 'There was a problem updating your profile. Please try again later')

        context = {'form': form}
        return render(request, 'account/profile.html', context)


class RegisterView(View):
    '''This class is for Authentication Register Account.'''

    def get(self, request):
        if not request.user.is_authenticated:
            form = RegisterForm()

            context = {'form': form}
            return render(request, 'account/register.html', context)
        else:
            return redirect('home')

    def post(self, request):
        if not request.user.is_authenticated:
            form = RegisterForm(request.POST)

            if form.is_valid():
                # create new user but not save in database !
                new_user = form.save(commit=False)
                # set the chosen password
                new_user.set_password(form.cleaned_data['password2'])
                # save user
                new_user.save()
                messages.success(request, 'Well done, created account!')

                # login to account
                cd = form.cleaned_data
                user_authentication = authenticate(
                    request,
                    username=cd['username'],
                    password=cd['password']
                )
                if user_authentication is not None:
                    if user_authentication.is_active:
                        login(request, user_authentication)
                        messages.info(request, 'Welcome to dashboard panel')
                        return redirect('dashboard')
                    else:
                        messages.info(request, 'Your account is disable!')
                else:
                    print(user_authentication)
                    messages.error(request, 'Oh snap! Information invalid , try again.')
                    return redirect('login')

            context = {'form': form}
            return render(request, 'account/register.html', context)
        else:
            return redirect('home')


class LoginView(View):
    '''This class is for Authentication Login Account.'''

    def get(self, request):
        if not request.user.is_authenticated:
            form = LoginForm()

            context = {'form': form}
            return render(request, 'account/login.html', context)
        else:
            return redirect('home')

    def post(self, request):
        if not request.user.is_authenticated:
            form = LoginForm(request.POST)

            if form.is_valid():
                cd = form.cleaned_data
                user_authentication = authenticate(
                    request,
                    username=cd['username'],
                    password=cd['password']
                )

                if user_authentication is not None:
                    if user_authentication.is_active:
                        login(request, user_authentication)
                        messages.success(request, 'Welcome to dashboard panel')
                        return redirect('dashboard')
                    else:
                        messages.info(request, 'Your account is disable!')
                else:
                    print(user_authentication)
                    messages.error(request, 'Oh snap! Information invalid , try again.')

            context = {'form': form}
            return render(request, 'account/login.html', context)
        else:
            return redirect('home')


class LogoutView(View):
    '''This class is for Authentication Logout Account.'''

    def get(self, request):
        if request.user.is_authenticated:
            username = request.user.get_username()
            logout(request)

            context = {'username': username}
            return render(request, 'account/logout.html', context)
        else:
            return redirect('home')


class PasswordChangeView(View):
    '''This class is for change password user account.'''

    def get(self, request):
        if request.user.is_authenticated:
            form = PasswordChangeForm(request.user)

            context = {'form': form}
            return render(request, 'account/password_change.html', context)
        else:
            return redirect('login')

    def post(self, request):
        if request.user.is_authenticated:
            form = PasswordChangeForm(request.user, request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Your password was successfully updated!')
                return redirect('dashboard')
            else:
                messages.error(request, 'Please correct the error  below')
        else:
            return redirect('login')
