# from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from ielex.profiles.forms import *
from ielex.shortcuts import render_template

@login_required
def view_profile(request, username=None):
    if username:
        the_user = get_object_or_404(User, username__exact=username)
    else:
        the_user = request.user
    return render_template(request, "profiles/view_profile.html",
            {"the_user":the_user})

@login_required
def alter_profile(request, username=None):
    if username:
        the_user = get_object_or_404(User, username__exact=username)
    else:
        the_user = request.user
    if request.method == 'POST':
        redirect_url = "/accounts/profile/"
        if the_user != request.user:
            redirect_url += the_user.username + "/"
        form = UserAlterDetailsForm(request.POST)
        if "cancel" in form.data: # has to be tested before data is cleaned
            return HttpResponseRedirect(redirect_url)
        assert form.is_valid()
        if form.is_valid():
            for key in form.cleaned_data:
                setattr(the_user, key, form.cleaned_data[key])
            the_user.save()
            return HttpResponseRedirect(redirect_url)
    else:
        form = UserAlterDetailsForm(the_user.__dict__)
    return render_template(request, "profiles/alter_profile.html",
            {"the_user":the_user,
             "form":form})

@login_required
def change_password(request):
    if request.method == 'POST':
        redirect_url = "/accounts/profile/"
        form = PasswordChangeForm(request.user, request.POST)
        if "cancel" in form.data: # has to be tested before data is cleaned
            return HttpResponseRedirect(redirect_url)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(redirect_url)
    else:
        form = PasswordChangeForm(request.user)
    return render_template(request, "profiles/change_password.html",
            {"form":form})

