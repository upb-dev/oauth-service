from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from oauth.app.models import User


class UserSerializer(serializers.ModelSerializer):
    authorities  = serializers.SerializerMethodField()
    
    def get_authorities(self, obj):
        permissions = obj.user_permissions.values_list('name')
        return permissions
    class Meta:
        model = User
        fields = ('id','email', "first_name", "last_name", "phone", "is_active",'authorities')

# TODO change register serializer
class RegisterSerializer(serializers.ModelSerializer):
    
    def validate_password(self, attrs):
        from django.contrib.auth.hashers import make_password
        return make_password(attrs)

    def validate(self, data):
        try:
            user = User.objects.filter(email=data.get('email'))
            if len(user) > 0:
                raise serializers.ValidationError(_("Email already exists"))
        except User.DoesNotExist:
            pass

        if not data.get('password') :
            raise serializers.ValidationError(_("Empty Password"))
        return data

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password', 'is_active')