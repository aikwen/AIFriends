from http.client import responses

from django.conf import settings
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken


class RefreshTokenView(APIView):
    def post(self, request):
        try:
            refresh_token = request.COOKIES.get('refresh_token')
            if not refresh_token:
                return Response(
                    {'result': 'refresh token 不存在'},
                status=status.HTTP_401_UNAUTHORIZED)
            # 如果过期了的话会报异常
            refresh = RefreshToken(refresh_token)
            if settings.SIMPLE_JWT['ROTATE_REFRESH_TOKENS']:
                refresh.set_jti()
                response = Response({
                    'result': 'success',
                    'access_token': str(refresh.access_token),
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
                'result': 'success',
            })
        except:
            return Response({
                'result': 'refresh token 过期了'
            },status=status.HTTP_401_UNAUTHORIZED)