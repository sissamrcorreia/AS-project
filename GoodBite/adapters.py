from allauth.account.adapter import DefaultAccountAdapter

class GoodBiteAccountAdapter(DefaultAccountAdapter):
    def get_reauthentication_timeout(self, request):
        return 1800