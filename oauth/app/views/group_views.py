
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _
from oauth2_provider.contrib.rest_framework import TokenHasScope
from rest_framework import generics, permissions

from oauth.app.serializers.group_serializers import GroupSerializer


class GroupList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated, TokenHasScope]
    required_scopes = ['groups']
    queryset = Group.objects.all()
    serializer_class = GroupSerializer