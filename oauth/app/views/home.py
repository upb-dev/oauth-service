from django.shortcuts import render
from django.conf import settings
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required()
def home(request):
    data = {
        "version": settings.VERSION
    }
    return render(request, 'home.html', data)