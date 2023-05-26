"""
URL configuration for oauth project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

from oauth.app.views.custom_token_views import CustomTokenView
from oauth.app.views.user_views import UserDetails, UserList, UserRegister
from oauth.app.views.home import home
from oauth.app.views.login_views import custom_login

urlpatterns = [
    path('', home, name="home"),
    path('admin/', admin.site.urls),
    path('accounts/login/', custom_login, name="login"),
    path('accounts/profile/', home, name="profile"),
    path('accounts/', include("django.contrib.auth.urls")),
    path('oauth/token/', CustomTokenView.as_view(), name='token'),
    path('oauth/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('users/', UserList.as_view()),
    path('users/<pk>/', UserDetails.as_view()),
    path('user/register/', UserRegister.as_view()),
]
