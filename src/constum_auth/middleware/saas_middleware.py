# app/middleware.py
from constum_auth.models import SaasUser
class SaasUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user_id = request.session.get("saas_user_id")
        request.saas_user = None
        if user_id:
            try:
                request.saas_user = SaasUser.objects.get(id=user_id)
            except SaasUser.DoesNotExist:
                pass
        return self.get_response(request)
