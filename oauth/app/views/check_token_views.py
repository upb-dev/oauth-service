from oauth2_provider.views.introspect import IntrospectTokenView
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
import calendar

from oauth2_provider.models import get_access_token_model


class CheckTokenView(IntrospectTokenView):
    @staticmethod
    def get_token_response(token_value=None):
        try:
            token = (
                get_access_token_model().objects.select_related("user", "application").get(token=token_value)
            )
        except ObjectDoesNotExist:
            return JsonResponse({"active": False}, status=200)
        else:
            if token.is_valid():
                data = {
                    "active": True,
                    "scope": token.scope,
                    "exp": int(calendar.timegm(token.expires.timetuple())),
                }
                authorities_application = list(token.application.user.groups.values_list('name'))

                if token.application:
                    data["client_id"] = token.application.client_id
                if token.user is not None:
                    user_authorities = list(token.user.groups.values_list('name'))
                    common_authorities = set(authorities_application) & set(user_authorities)
                    data["username"] = token.user.get_username()
                    data['user_id'] = str(token.user.id)
                    data['email'] = token.user.email
                    data['phone_no'] = token.user.phone
                    data['authorities'] = list(map(lambda tpl: tpl[0], common_authorities))
                else:
                    data['authorities'] = list(map(lambda tpl: tpl[0], authorities_application))

                return JsonResponse(data)
            else:
                return JsonResponse({"active": False}, status=200)
