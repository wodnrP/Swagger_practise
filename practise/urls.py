from django.urls import path
from .import views
from .views import SignupAPIView, LoginAPIView, LogoutAPIView, UserAPIView, RefreshAPIView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('signup', SignupAPIView.as_view()),        # 회원가입
    path('login', LoginAPIView.as_view()),          # 로그인
    path('logout', LogoutAPIView.as_view()),         # 로그아웃
    path('user-info', UserAPIView.as_view()),        # 유저 정보 조회/업데이트
    path('refresh', RefreshAPIView.as_view()),      # refresh_token으로 토큰 갱신
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)