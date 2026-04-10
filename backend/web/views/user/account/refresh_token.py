import jwt
from django.conf import settings
from rest_framework import status
from  rest_framework.views import APIView
from rest_framework.response import Response

class RefreshToken(APIView):
    def post(self, request):
        try:
            refresh_token = request.COOKIES.get('refresh_token')
            if not refresh_token:
                return Response({
                    'result':'refresh token不存在',
                },status=401) #必须加，前端判断用得到
            refresh = RefreshToken(refresh_token) #自动检查refresh,如果过期，会报异常
            if settings.SIMPLE_JWT['ROTATE_REFRESH_TOKENS']:
                refresh.set_jti()
                response = Response({
                    'result':'success',
                    'access': str(refresh.access_token),
                })
                response.set_cookie(
                    key='refresh_token',
                    value=str(refresh),
                    httponly=True,
                    samesite='Lax',
                    secure=True,
                    max_age=86400 * 7,
                )
                return response
            return Response({
                'result':'success',
                'access': str(refresh.access_token),
            })

        except:
            return Response({
                'result':'refresh token 过期了',
            },status=401) #必须加，前端判断用得到