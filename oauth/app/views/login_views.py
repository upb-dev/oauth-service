from django.views import View
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
# logot view bisa diambil dari sini
from django.contrib.auth import views as auth_views


def custom_login(request):
    if request.method == "GET" and request.user.is_authenticated:
        return redirect('profile')
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Logika tambahan sebelum autentikasi
        # Misalnya, validasi tambahan atau manipulasi data

        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            # Redirect ke halaman setelah login berhasil
            return redirect('profile')
        else:
            # Autentikasi gagal, tampilkan pesan kesalahan
            error_message = "Please enter a correct email and password. Note that both fields may be case-sensitive."
            return render(request, 'registration/login.html', {'error_message': error_message})

    return render(request, 'registration/login.html')
