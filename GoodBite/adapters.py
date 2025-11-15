from allauth.account.adapter import DefaultAccountAdapter
from allauth.mfa.adapter import get_adapter as get_mfa_adapter


class GoodBiteAccountAdapter(DefaultAccountAdapter):
    """
    Después de login:
    - Si el usuario NO tiene MFA, se lo redirige a /accounts/2fa/
    - Si ya tiene MFA, se usa el comportamiento normal (LOGIN_REDIRECT_URL)
    """

    def get_login_redirect_url(self, request):
        user = request.user
        mfa_adapter = get_mfa_adapter()

        if user.is_authenticated and not mfa_adapter.is_mfa_enabled(user):
            # Página de gestión/activación MFA
            return "/accounts/2fa/"

        # Comportamiento normal de allauth (irá a LOGIN_REDIRECT_URL, que es 'home')
        return super().get_login_redirect_url(request)
