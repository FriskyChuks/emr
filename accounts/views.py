from django.contrib.auth import authenticate, login, get_user_model, logout
from django.urls import reverse
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.utils.http import is_safe_url
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import User
from .forms import ContactForm, LoginForm, RegisterForm

from .decorators import allowed_users


@login_required
# @unauthenticated_user
# @allowed_users(alllowed_roles=['admin'])
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

# @unauthenticated_user
def login_view(request):
    userlogin = request.user
    if request.method == "POST":
        username_var = request.POST.get('username')
        password_var = request.POST.get('password')
        user = authenticate(request,username=username_var, password=password_var)

        qs = User.objects.filter(username=username_var)
        if len(qs) < 1:
            messages.warning(request, "This user does not EXIST!")
        
        try:
            user = User.objects.get(username=username_var)
        except:
            user = None
        if user is not None and not user.check_password(password_var):
            messages.warning(request, "Wrong password")
        elif user is None:
            pass
        else:     
            login(request, user)
            messages.success(request, "Welcome" + " " + str(userlogin))
            if "next" in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return HttpResponseRedirect("/home")
                # clinic_id = request.user.clinic_id
                # group_name = request.user.group.name
                # if (clinic_id  and group_name == "doctor") or (clinic_id and group_name == "nurse"):
                #     return redirect("clinic_visits_display", id=clinic_id)
                # elif group_name == "MLS":
                #     return HttpResponseRedirect("/labs/request_list_view")
                # else:
                #     return HttpResponseRedirect("/home")

    context = {}
    return render(request, 'accounts/login2.html', context)


def logout_view(request):
    logout(request)
    # messages.success(request, "Sad to see you leave! See you soon please!")
    return HttpResponseRedirect('%s'%(reverse("auth_login")))