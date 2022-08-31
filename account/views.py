from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin

from cart.cart import Cart
from .forms import LoginUserForm


class UserLoginView(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('wagtail_')
        else:
            form = LoginUserForm()
            return render(request, 'account/login.html', {'form': form})

    def post(self, request, *args, **kwargs):
        session_old = request.session
        form = LoginUserForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(email=cd['email'], password=cd['password'])
            if user is not None:
                login(request, user)
                Cart(request, new_session=session_old)
                return redirect('/')

        else:
            messages.error(request, 'Неверный логин или пароль!')
            return redirect('account:login')


class AccountProfile(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'login'

    def get(self, request, *args, **kwargs):
        return render(request, 'account/profile.html')
