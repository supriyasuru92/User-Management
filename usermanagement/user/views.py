from django.shortcuts import render, redirect
from .forms import *
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from .profile import size_compress


@login_required
def home(request):
    user = User.objects.get(username=request.user)
    all_users = User.objects.filter().exclude(is_staff=True).exclude(username=request.user)
    return render(request=request, template_name='user/index.html', context={'user': user, 'all_users': all_users})


def register(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("homepage")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(request=request, template_name="user/register.html", context={"register_form": form})


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("homepage")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="user/login.html", context={"login_form": form})


def logout_view(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("login")


@login_required
def delete_user(request, id):
    user = User.objects.filter(id=id)
    if user:
        user.delete()
        messages.success(request, f'Your user has been deleted!')
    return redirect('homepage')  # Redirect back to homepage page


@login_required
def profile(request):
    user_profile = Profile.objects.filter(user=request.user)
    if request.method == 'POST':
        try:
            profile = request.user.profile
        except Profile.DoesNotExist:
            profile = Profile(user=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if p_form.is_valid():
            p_form.save()
            size_compress(request.user)
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')  # Redirect back to profile page
    else:
        if user_profile:
            p_form = ProfileUpdateForm(instance=request.user.profile)
        else:
            p_form = ProfileUpdateForm()

    context = {
        'p_form': p_form
    }

    return render(request, 'user/profile.html', context)


@login_required
def delete_profile(request):
    user_profile = Profile.objects.filter(user=request.user)
    if user_profile:
        request.user.profile.delete()
        messages.success(request, f'Your profile has been deleted!')
    else:
        return HttpResponse("you have no saved profile.")
    return redirect('homepage')
