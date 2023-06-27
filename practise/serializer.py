from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'profile', 'nickname')

    # 유저 password 암호화하여 DB저장
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
    
    # 유저 정보 변경 - UserAPIView patch와 연관
    def update(self, user, validated_data):
        # 수정된 정보일 경우만 저장
        if 'password' in self.validated_data: 
            if user.password != self.validated_data['password']:
                user.set_password(validated_data['password'])
        if 'profile' in self.validated_data: 
            if user.profile != self.validated_data['profile']:
                user.profile = validated_data.get('profile', user.profile)
        if 'nickname' in self.validated_data:
            if user.nickname != self.validated_data['nickname']:
                user.nickname = validated_data.get('nickname', user.nickname)
        user.save()
        return user

# swagger request body custom serializer    
class LoginUserSerializer(serializers.Serializer):
    username = serializers.CharField(help_text="아이디")
    password = serializers.CharField(help_text="패스워드")

class UserUpdateSerializer(serializers.Serializer):
    password = serializers.CharField(help_text="패스워드")
    nickname = serializers.CharField(help_text="닉네임")
    profile = serializers.ImageField(help_text="프로필이미지")

class RefreshSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(help_text="refresh_token")