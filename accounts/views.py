from django.contrib.auth import authenticate, login, get_user_model, logout
from django.urls import reverse
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.utils.http import url_has_allowed_host_and_scheme
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import User, Group
from .forms import ContactForm, LoginForm, RegisterForm
from patients.models import State

from .decorators import allowed_users


@login_required
# @unauthenticated_user
@allowed_users(alllowed_roles=['admin'])
def registration_view(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():  # and profile_form.is_valid():
        new_user = form.save()
        new_user.save()

        return HttpResponseRedirect("/accounts/login")

    context = {
        "form": form,  # 'profile_form': profile_form
    }
    return render(request, 'accounts/register.html', context)


def login_view(request):
    Group.objects.get_or_create(name='user')
    userlogin = request.user
    if request.method == "POST":
        username_var = request.POST.get('username')
        password_var = request.POST.get('password')
        user = authenticate(request, username=username_var,
                            password=password_var)

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
                clinic_id = request.user.clinic_id
                group_name = request.user.group.name
                if (clinic_id and group_name == "doctor") or (clinic_id and group_name == "nurse"):
                    return redirect("clinic_visits_display", id=clinic_id)
                elif group_name == "MLS":
                    return HttpResponseRedirect("/labs/request_list_view")
                elif group_name == "radiology":
                    return HttpResponseRedirect("/radiology/pending_rad_request")
                elif group_name == "cashier":
                    return HttpResponseRedirect("/bills/billing_home")
                else:
                    return HttpResponseRedirect("/home")

    context = {}
    return render(request, 'accounts/login.html', context)


@login_required
def account_setting_view(request, user_id):
    user = User.objects.get(id=user_id)
    states = State.objects.all().order_by('title')

    if request.method == 'POST':
        print(request.POST.get('gender'))
        User.objects.filter(id=request.user.id).update(
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            email=request.POST.get('email'),
            phone1=request.POST.get('phone1'),
            gender=request.POST.get('gender'),
            image=request.POST.get('image')
        )

    template = 'home/settings.html'
    context = {"user": user, "states": states}
    return render(request, template, context)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('%s' % (reverse("auth_login")))
