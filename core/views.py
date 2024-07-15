from django.shortcuts import render
from .models import *
from django.template.loader import render_to_string
from django.http import JsonResponse
from .forms import *
from django.shortcuts import render, redirect
from django.contrib import messages

# Create your views here.


def home(request):
    return render(request, 'core/home.html')




def about(request):
    return render(request, 'core/about.html')



def contact(request):
    if request.method == 'POST':
        form = ContactUsForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('success')  # Success view or URL name
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = ContactUsForm()
    return render(request, 'core/contact.html', {'form': form})




def custom_404_page(request, exception):
    return render(request, 'errors/404.html' ,status=404)

def custom_500_page(request):
    return render(request, 'errors/500.html', status=500)


