from rest_framework import serializers
from .serializer import UserSerializer
from drf_yasg import openapi

# swagger request body custom serializer    
# 로그인 request body parameters
class LoginUserSerializer(serializers.Serializer):
    username = serializers.CharField(help_text="아이디")
    password = serializers.CharField(help_text="패스워드")

# 사용자 정보 수정 request body parameters
class UserUpdateSerializer(serializers.Serializer):
    password = serializers.CharField(help_text="패스워드", required=False)
    nickname = serializers.CharField(help_text="닉네임", required=False)
    profile = serializers.ImageField(help_text="프로필이미지", required=False)

# 로그인 refresh request body parameters
class RefreshSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(help_text="refresh_token")

# 사용자 정보 조회/수정 헤더 
UserinfoHeader=[
    openapi.Parameter(
        'Authorization', 
        openapi.IN_HEADER, 
        description="Authorization bearer access_token", 
        type=openapi.TYPE_STRING
        )
    ]

# 회원가입/로그인 response
SignupResponse = {
    201: openapi.Response(
        description="201 OK", 
        schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties = {
            'access_token': openapi.Schema(type=openapi.TYPE_STRING, description="access_token"),
            'access_exp': openapi.Schema(type=openapi.TYPE_STRING, description="access_exp"),
            'refresh_token': openapi.Schema(type=openapi.TYPE_STRING, description="refresh_token"),
            }
        )),
            400: 'KeyNotFound',
            500: 'Server Error'
}

# 로그아웃 response
LogoutResponse = {
    200: openapi.Response(
        description="200 OK",
        schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties = {
            'Message': openapi.Schema(type='Logout success', description="로그아웃 성공 메시지")
            }
        ))
    }

# 사용자 정보 조회 response
GetUserResponse = {
    200: openapi.Response(
        description="200 OK",
        schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties = {
            'id': openapi.Schema(type=openapi.TYPE_INTEGER, description="id"),
            'profile': openapi.Schema(type=openapi.TYPE_STRING, description="profile"),
            'nickname': openapi.Schema(type=openapi.TYPE_STRING, description="nickname")
            }
        )),
    401: 'unauthenticated',
    500: 'Server Error'
    }

# 사용자 정보 수정 response
UpdateUserResponse = {
    200: openapi.Response(
        description="200 OK",
        schema=UserSerializer
        ),
    401: 'unauthenticated',
    500: 'Server Error'
    }

# refresh 로그인 response
RefreshResponse = {
    201: openapi.Response(
        description="201 OK",
        schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties = {
            'access_token': openapi.Schema(type=openapi.TYPE_STRING, description="access_token"),
            'access_exp': openapi.Schema(type=openapi.TYPE_STRING, description="access_exp")
        }
    ))
}