from django.shortcuts import redirect, render


def profile(request):
    if request.method == "GET" and not request.user.is_authenticated:
        return redirect('login')

    return render(request=request,  template_name='profile.html', context={'user': request.user})
