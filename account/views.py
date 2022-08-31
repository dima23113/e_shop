from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.mixins import LoginRequiredMixin

from cart.cart import Cart
from product.recently_product import RvProduct
from .forms import LoginUserForm, PasswordChangeForm
from .models import CustomUser


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


class UserLogoutView(LoginRequiredMixin, View):
    redirect_field_name = 'login'

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('/')


class UserChangePassword(LoginRequiredMixin, View):
    redirect_field_name = 'login'

    def get(self, request, *args, **kwargs):
        context = {
            'form': PasswordChangeForm(),
        }
        return render(request, 'account/change_password.html', context=context)

    def post(self, request, *args, **kwargs):
        form = PasswordChangeForm(request.POST)
        if form.is_valid():
            user = CustomUser.objects.get(email=request.user)
            cd = form.cleaned_data
            if check_password(cd['password_now'], user.password):
                if cd['password'] == cd['password1']:
                    user.set_password(cd['password'])
                    user.save()
                    login(request, user)
                    return redirect('/')
                else:
                    messages.add_message(request, messages.INFO,
                                         'Повторный пароль некорректен!')
                    return redirect('account:change_password')
            else:
                messages.add_message(request, messages.INFO,
                                     'Текущий пароль не верен!')
                return redirect('account:change_password')
        else:
            return redirect('account:change_password')


class AccountProfile(LoginRequiredMixin, View):
    redirect_field_name = 'login'

    def get(self, request, *args, **kwargs):
        context = {
            'rv_products': RvProduct(request)
        }
        return render(request, 'account/profile.html', context=context)
