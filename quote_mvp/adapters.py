from allauth.account.adapter import DefaultAccountAdapter
from django.shortcuts import resolve_url
from allauth.socialaccount.models import SocialAccount

class CustomAccountAdapter(DefaultAccountAdapter):
    def get_login_redirect_url(self, request):
        user = request.user

        if user.is_authenticated:
            try:
                social = SocialAccount.objects.get(user=user)
                if not user.ruc or not user.company or not user.rol:
                    return resolve_url("users:register")
            except SocialAccount.DoesNotExist:
                pass

        return resolve_url("users:register")
