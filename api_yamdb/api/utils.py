from rest_framework_simplejwt.tokens import AccessToken


def get_token_for_user(user):
    token = AccessToken.for_user(user)
    return {
        'token': str(token)
    }
