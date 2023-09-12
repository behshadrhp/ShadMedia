from django.views import View
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import authenticate, login

from .forms import LoginForm


class AuthenticationView(View):
    '''This class is for Authentication Account.'''

    def get(self, request):
        form = LoginForm()

        context = {'form': form}
        return render(request, 'account/login.html', context)

    def post(self, request):
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
                else:
                    messages.info(request, 'Your account is disable!')
            else:
                messages.error(request, 'Oh snap! Information invalid , try again.')

        context = {'form': form}
        return render(request, 'account/login.html', context)   
