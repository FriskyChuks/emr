from django.contrib.auth import authenticate, login, get_user_model, logout
from django.db.models.aggregates import Count
from django.views.generic import CreateView, FormView
from django.http import HttpResponse
from django.urls import reverse
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.utils.http import is_safe_url

from .forms import ContactForm, LoginForm, RegisterForm


def registration_view(request):
    form = RegisterForm(request.POST or None)
    # profile_form = RegisterForm(request.POST or None)
    if form.is_valid():# and profile_form.is_valid():
        new_user = form.save()
        new_user.save()

        return HttpResponseRedirect("/accounts/login")

    context = {
        "form": form,# 'profile_form': profile_form
    }
    return render(request, 'accounts/register.html', context)


def login_view(request):
    form = LoginForm(request.POST or None)
    userlogin = request.user
    if form.is_valid():
        username_var = (form.cleaned_data['username'])
        password_var = (form.cleaned_data['password'])
        user = authenticate(username=username_var, password=password_var)
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        # messages.success(request, "Welcome" + " " + str(userlogin))
        if "next" in request.POST:
            return redirect(request.POST.get('next'))
        else:
            return HttpResponseRedirect("/home")

        # if user.is_superuser:
        #     return HttpResponseRedirect("/")
        # else:
        #     return HttpResponseRedirect("/logout")
    context = {
        "form": form
    }
    return render(request, 'accounts/login.html', context)


def logout_view(request):
    logout(request)
    # messages.success(request, "Sad to see you leave! See you soon please!")
    return HttpResponseRedirect('%s'%(reverse("auth_login")))
