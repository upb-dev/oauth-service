from django.http import HttpResponse
from oauth2_provider.views.base import TokenView
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from oauth2_provider.models import get_access_token_model, get_application_model
from oauth2_provider.signals import app_authorized
import json

class CustomTokenView(TokenView):
    @method_decorator(sensitive_post_parameters("password"))
    def post(self, request, *args, **kwargs):
        url, headers, body, status = self.create_token_response(request)
        if status == 200:
            body = json.loads(body)
            access_token = body.get("access_token")
            if access_token is not None:
                token = get_access_token_model().objects.get(
                    token=access_token)
                app_authorized.send(
                    sender=self, request=request,
                    token=token)
                
                body['member'] = {
                    'user_id': str(token.user.id), 
                    'username': token.user.username, 
                    'user_email': token.user.email,
                    'user_phone_no': token.user.phone
                }
                body = json.dumps(body) 
        response = HttpResponse(content=body, status=status)
        for k, v in headers.items():
            response[k] = v
        return response