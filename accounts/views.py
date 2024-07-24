from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm,PasswordChangeForm
from django.contrib import messages
from .forms import SignUpForm
from actstream import action
from django.contrib.auth.decorators import login_required
from language.utils import get_translation
from django.utils import translation
from django.conf import settings
from translateContext.translateContext import *

def signup_view(request):
    mainContext = get_trans_lang(request)
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('core:home')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = SignUpForm()
        context = {
            "form":form
        }
        mainContext.update(context)
    return render(request, 'accounts/signup.html', mainContext)

def signin_view(request):
    mainContext = get_trans_lang(request)
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Logged in successfully!')
                return redirect('core:home')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = AuthenticationForm()
        context = {
            "form":form
        }
        mainContext.update(context)
    return render(request, 'accounts/signin.html', mainContext)


@login_required(login_url='accounts:signin')
def change_password(request):
    mainContext = get_trans_lang(request)
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('profile:profile')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")
    else:
        form = PasswordChangeForm(request.user)

    context = {
        "form": form,
    }
    
    mainContext.update(context)
    return render(request, 'profiles/change_password.html', mainContext)



