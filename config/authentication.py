import jwt
from users.models import User
from rest_framework import authentication

from config import settings


class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        try:

            token = request.META.get('HTTP_AUTHORIZATION')
            if token is None:
                return None
            xjwt, token_jwt = token.split(' ')
            decoded = jwt.decode(token_jwt, settings.SECRET_KEY, algorithms=['HS256'])
            pk = decoded.get('pk')
            user = User.objects.get(pk=pk)
            print(user)
            return (user, None)
        except (ValueError, jwt.exceptions.DecodeError, User.DoesNotExist):
            return None
