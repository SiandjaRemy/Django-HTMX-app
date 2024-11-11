from allauth.account.adapter import DefaultAccountAdapter

class CustomAccountAdapter(DefaultAccountAdapter):
    def get_signup_redirect_url(self, request):
        # Define your custom redirect URL here
        return '/profile/onboarding/'
    
# 987654321@