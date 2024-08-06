from .models import *
from django.template.loader import render_to_string
from django.http import JsonResponse
from .forms import *
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from language.utils import get_translation
from django.utils import translation
from django.conf import settings
from translateContext.translateContext import *
from django.core.mail import EmailMessage
from django.contrib.auth import login
from django.contrib.auth.models import User

# Create your views here.


def home(request):
    mainContext = get_trans_lang(request)

    return render(request, 'core/home.html', mainContext)




def about(request):
    mainContext = get_trans_lang(request)
    return render(request, 'core/about.html', mainContext)



def contact(request):
    mainContext = get_trans_lang(request)

    if request.method == 'POST':
        form = ContactUsForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('core:contact')  # Success view or URL name
        
    else:
        form = ContactUsForm()
        context={
            "form":form
        }
        mainContext.update(context)
    return render(request, 'core/contact.html', mainContext)




def custom_404_page(request, exception):
    return render(request, 'errors/404.html' ,status=404)

def custom_500_page(request):
    return render(request, 'errors/500.html', status=500)












################### Forgot Passwords Open ################


def forgot_password(request):
    mainContext = get_trans_lang(request)

    if request.method=="POST":
        un = request.POST["username"]
        pwd = request.POST["npass"]

        user = get_object_or_404(User,username=un)
        user.set_password(pwd)
        user.save()

        login(request,user)
        user_name = request.user.username 
        context1 = {
            'success_messages': f"Şifren başarıyla değiştirildi. Tekrar hoşgeldin, {user_name}!",
            'target_url':"main:home",
        }
        context1.update(mainContext)
        return render(request, "core/home.html", context1)
    return render(request,"accounts/forgot_password.html",mainContext)


import random

def reset_password(request):
    username = request.GET.get("username")
    mainContext = get_trans_lang(request)
    try:
        user = get_object_or_404(User, username=username)
        otp = random.randint(100000, 999999)
        context = {
            'username': user.username,
            'otp': otp,
        }
        context.update(mainContext)
        email_content = render_to_string('email_templates/reset_password_email.html', context)
        try:
            email = EmailMessage("Hesap Doğrulama", email_content, to=[user.email])
            email.content_subtype = 'html' 
            email.send()
            return JsonResponse({"status": "sent", "email": user.email, "rotp": otp})
        except Exception as e:
            return JsonResponse({"status": "error", "email": user.email, "errordetail1": str(e)})
    except Exception as e:
        return JsonResponse({"status": "failed", "errordetail": str(e)})
    
################### Forgot Passwords Close ################################### Forgot Passwords Open ################

