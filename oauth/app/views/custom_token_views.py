import json

from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from oauth2_provider.models import get_access_token_model
from oauth2_provider.signals import app_authorized
from oauth2_provider.views.base import TokenView


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
                authorities_application = list(token.application.user.groups.values_list('name'))

                if token.user is not None:
                    user_authorities = list(token.user.groups.values_list('name'))
                    common_authorities = set(authorities_application) & set(user_authorities)
                    body['user_id'] = str(token.user.id)
                    body['email'] = token.user.email
                    body['phone_no'] = token.user.phone
                    body['authorities'] = list(map(lambda tpl: tpl[0], common_authorities))
                else:
                    body['authorities'] = list(map(lambda tpl: tpl[0], authorities_application))

                body = json.dumps(body)
        response = HttpResponse(content=body, status=status)
        for k, v in headers.items():
            response[k] = v
        return response
