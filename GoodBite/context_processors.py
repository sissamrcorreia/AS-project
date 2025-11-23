from allauth.mfa.adapter import get_adapter

def mfa_status(request):
    """
    Context processor que añade is_mfa_enabled a todas las plantillas
    """
    is_mfa_enabled = False

    if request.user.is_authenticated:
        adapter = get_adapter()
        is_mfa_enabled = adapter.is_mfa_enabled(request.user)

    return {
        'is_mfa_enabled': is_mfa_enabled,
    }