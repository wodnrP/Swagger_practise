from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import APIException, AuthenticationFailed
from rest_framework.authentication import get_authorization_header
from .authentication import create_access_token, create_refresh_token, decode_access_token, decode_refresh_token, access_token_exp
from .serializer import UserSerializer, LoginUserSerializer, UserUpdateSerializer, RefreshSerializer
from .models import User
from django.utils import timezone
from rest_framework import permissions
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.parsers import MultiPartParser
# Create your views here.

# 회원가입 에러 처리
class SignupException(APIException):
    status_code = 400
    default_detail = '실패! 입력한 정보를 다시 확인해주세요'
    default_code = 'KeyNotFound'

# 로그인 에러 처리 
class LoginException(APIException):
    status_code = 400
    default_detail = '아이디 혹은 비밀번호를 다시 확인해주세요'
    default_code = 'KeyNotFound'

# 로그인시 토큰 생성 함수
def token_create(user):    
    access_token = create_access_token(user.id)
    access_exp = access_token_exp(access_token)
    refresh_token = create_refresh_token(user.id)

    response = Response()
    response.set_cookie(key='refreshToken', value=refresh_token, httponly=True)         #리프레쉬 토큰 쿠키에 저장
    response.data = {
        'access_token' : access_token,
        'access_exp' : access_exp,
        'refresh_token' : refresh_token
    }
    return response

# 회원가입 API (회원가입시 즉시 로그인)
class SignupAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        # operation_description= API 설명
        # operation_summary= API 간단 타이틀, 통합하는 주제
        # operation_id= API 구분하는 고유 값 (중복의 가능성있기 때문에 신경써야함)
        tags=["사용자 회원가입"], 
        request_body=UserSerializer,
        responses = {
            201: openapi.Response(
                description="201 OK", 
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties = {
                        'access_token': openapi.Schema(type=openapi.TYPE_STRING, description="access_token"),
                        'access_exp': openapi.Schema(type=openapi.TYPE_STRING, description="access_exp"),
                        'refresh_token': openapi.Schema(type=openapi.TYPE_STRING, description="refresh_token"),
                    }
                )
            ),
            400: 'KeyNotFound',
            500: 'Server Error'
        }
        )
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

            user = User.objects.filter(username=request.data['username']).first()
            
            # 중복되는 유저가 있는지 확인
            if not user:
                raise SignupException()
            if not user.check_password(request.data['password']):
                raise SignupException()

            # 가입한 유저 토큰 생성 및 로그인
            return token_create(user)

# 로그인 API
class LoginAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        tags=["로그인"], 
        request_body=LoginUserSerializer, 
        responses = {
            201: openapi.Response(
                description="201 OK", 
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties = {
                        'access_token': openapi.Schema(type=openapi.TYPE_STRING, description="access_token"),
                        'access_exp': openapi.Schema(type=openapi.TYPE_STRING, description="access_exp"),
                        'refresh_token': openapi.Schema(type=openapi.TYPE_STRING, description="refresh_token"),
                    }
                )
            ),
            400: 'KeyNotFound',
            500: 'Server Error'
        }
    )
    def post(self, request):
        user = User.objects.filter(username=request.data['username']).first()
        if not user:
            raise LoginException()
        if not user.check_password(request.data['password']):
            raise LoginException()
        
        return token_create(user)

# 로그아웃 API
class LogoutAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
            tags=["로그아웃"],
            responses = {
                200: openapi.Response(
                    description="200 OK",
                    schema=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties = {
                            'Message': openapi.Schema(type='Logout success', description="로그아웃 성공 메시지")
                        }
                    )
                )
            }
                        )
    def delete(self, _):
        response = Response()
        response.delete_cookie(key="refreshToken")
        response.data = {
            'Message' : 'Logout success'
        }
        return response

# auth token 복호화 : id return
def token_decode(auth):
    token = auth[1].decode('utf-8')
    id = decode_access_token(token)
    return id

# 유저정보 조회 및 수정 API
class UserAPIView(APIView):
    permission_classes = [permissions.AllowAny]
    parser_classes=(MultiPartParser,) #이미지 fields 나타나지 않는 에러 해결
    # 유저정보 조회
    @swagger_auto_schema(
            tags=["사용자 정보 조회"],
            manual_parameters=[
                openapi.Parameter(
                    'Authorization', 
                    openapi.IN_HEADER, 
                    description="Authorization bearer access_token", 
                    type=openapi.TYPE_STRING
                    )
                ],
            responses = {
                200: openapi.Response(
                    description="200 OK",
                    schema=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties = {
                            'id': openapi.Schema(type=openapi.TYPE_INTEGER, description="id"),
                            'profile': openapi.Schema(type=openapi.TYPE_STRING, description="profile"),
                            'nickname': openapi.Schema(type=openapi.TYPE_STRING, description="nickname")
                            }
                        )
                    ),
                400: 'KeyNotFound',
                500: 'Server Error'
                }
            )
    def get(self, request, **kwargs):
        if kwargs.get('id') is None:
            auth = get_authorization_header(request).split()
            if auth and len(auth) == 2:
                user = User.objects.filter(pk=token_decode(auth)).first()
                return Response(UserSerializer(user).data, status=status.HTTP_200_OK)
            raise AuthenticationFailed('Unauthenticated')
            
        else:
            user_id = kwargs.get('id')
            user_serializer = UserSerializer(User.objects.get(pk=user_id))
            response = Response()

            user_id = user_serializer.data.get('id')
            nickname = user_serializer.data.get('nickname')
            profile =  user_serializer.data.get('profile')
            response.data = {
                'id' : user_id,
                'nickname' : nickname,
                'profile' : profile
            }
            return response

    # 유저정보 수정
    @swagger_auto_schema(
            tags=["사용자 정보 수정"],
            manual_parameters=[
                openapi.Parameter(
                    'Authorization', 
                    openapi.IN_HEADER, 
                    description="Authorization bearer access_token", 
                    type=openapi.TYPE_STRING
                    )
                ], 
            request_body=UserUpdateSerializer,
            responses = {
                200: openapi.Response(
                    description="200 OK",
                    schema=UserSerializer
                    ),
                400: 'KeyNotFound',
                500: 'Server Error'
                }
            )
    def patch(self, request):
        auth = get_authorization_header(request).split()
        if auth and len(auth) == 2:
            user = User.objects.filter(pk=token_decode(auth)).first()
            serializer = UserSerializer(user, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
# refresh login
class RefreshAPIView(APIView):
    permission_classes = [permissions.AllowAny]
    
    @swagger_auto_schema(
            tags=["로그인 세션 유지 : Access_Token 재발급"],
            request_body=RefreshSerializer,
            responses = {
                201: openapi.Response(
                    description="201 OK",
                    schema=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties = {
                            'access_token': openapi.Schema(type=openapi.TYPE_STRING, description="access_token"),
                            'access_exp': openapi.Schema(type=openapi.TYPE_STRING, description="access_exp")
                        }
                    )
                )
            }
        )
    def post(self, request):
        token = request.data['refresh_token']
        
        byt_token = bytes(token, 'utf-8')

        id = decode_refresh_token(byt_token)
        access_token = create_access_token(id)
        access_exp = access_token_exp(access_token)
        return Response({
            'access_token': access_token,
            'access_exp': access_exp
        })
