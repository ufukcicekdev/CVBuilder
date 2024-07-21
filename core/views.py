from django.shortcuts import render
from .models import *
from django.template.loader import render_to_string
from django.http import JsonResponse
from .forms import *
from django.shortcuts import render, redirect
from django.contrib import messages
from language.utils import get_translation
from django.utils import translation
from django.conf import settings
from translateContext.translateContext import *
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
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
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


