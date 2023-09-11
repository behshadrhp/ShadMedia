from django.views import View
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login

from .forms import LoginForm


class AuthenticationView(View):
    '''This class is for Authentication Account.'''

    def get(self, request):
        form = LoginForm()
        successfully = False
        disable = False
        invalid = False

        context = {'form': form, 'successfully': successfully, 'disable': disable, 'invalid': invalid}
        return render(request, 'account/login.html', context)

    def post(self, request):
        form = LoginForm(request.POST)

        successfully = False
        disable = False
        invalid = False

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
                    successfully = True
                else:
                    disable = True
            else:
                invalid = True

        context = {'form': form, 'successfully': successfully, 'disable': disable, 'invalid': invalid}
        return render(request, 'account/login.html', context)   
