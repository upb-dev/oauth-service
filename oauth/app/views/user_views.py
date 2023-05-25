from django.contrib import admin
from django.contrib.auth.models import Group

from oauth.app.models import User

admin.autodiscover()

import json

from braces.views import CsrfExemptMixin
from django.db import transaction
from django.utils.translation import gettext_lazy as _
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope
from oauth2_provider.settings import oauth2_settings
from oauth2_provider.views.mixins import OAuthLibMixin
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from oauth.app.serializers.user_serializers import (RegisterSerializer,
                                                    UserSerializer)


# Create the API views
class UserList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    

    def list(self, request, *args, **kwargs):
        
        return super().list(request, *args, **kwargs)

class UserDetails(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    queryset = User.objects.all()
    serializer_class = UserSerializer



class UserRegister(CsrfExemptMixin, OAuthLibMixin, APIView):
    permission_classes = (permissions.AllowAny,)

    server_class = oauth2_settings.OAUTH2_SERVER_CLASS
    validator_class = oauth2_settings.OAUTH2_VALIDATOR_CLASS
    oauthlib_backend_class = oauth2_settings.OAUTH2_BACKEND_CLASS
  
    # TODO change post function
    def post(self, request):
        if request.auth is None:
            data = request.data
            serializer = RegisterSerializer(data=data)
            if serializer.is_valid():
                try:
                    with transaction.atomic():
                        user = serializer.save()

                        # url, headers, body, token_status = self.create_token_response(request)
                        # if token_status != 200:
                        #     raise Exception(json.loads(body).get("error_description", ""))

                        return Response(serializer.data, status=200)
                except Exception as e:
                    return Response(data={"error": "error"}, status=status.HTTP_400_BAD_REQUEST)
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_403_FORBIDDEN) 