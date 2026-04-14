from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import timedelta


class RefreshTokenView(APIView):
    def post(self, request):
        try:
            refresh_token = request.COOKIES.get('refresh_token')
            if not refresh_token:
                return Response({
                    'result': 'refresh token不存在',
                }, status=401)

            refresh = RefreshToken(refresh_token)

            if settings.SIMPLE_JWT.get('ROTATE_REFRESH_TOKENS', False):
                refresh.set_jti()

                response = Response({
                    'result': 'success',
                    'access': str(refresh.access_token),
                })

                refresh_lifetime = settings.SIMPLE_JWT.get(
                    'REFRESH_TOKEN_LIFETIME',
                    timedelta(days=7)
                )

                secure = not settings.DEBUG

                response.set_cookie(
                    key='refresh_token',
                    value=str(refresh),
                    httponly=True,
                    samesite='Lax',
                    secure=secure,
                    max_age=int(refresh_lifetime.total_seconds()),
                )
                return response

            return Response({
                'result': 'success',
                'access': str(refresh.access_token),
            })

        except:
            return Response({
                'result': 'refresh token 过期了',
            }, status=401)