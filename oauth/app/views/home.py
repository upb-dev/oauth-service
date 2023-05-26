from django.shortcuts import render
from django.conf import settings

# Create your views here.

def home(request):
    is_login: bool = False
    if request.user.is_authenticated:
        is_login= True
    data = {
        "is_login": is_login,
        "version": settings.VERSION
    }
    return render(request, 'home.html', data)