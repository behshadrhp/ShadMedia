from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from .forms import LoginForm


class HomeView(View):
    '''This class is for return home page.'''

    def get(self, request):
        username = request.user.get_username()

        context = {'username': username}
        return render(request, 'home.html', context)


class AuthenticationView(View):
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
                        messages.success(request, 'Well done, login is successfully')
                        return redirect('home')
                    else:
                        messages.info(request, 'Your account is disable!')
                else:
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
