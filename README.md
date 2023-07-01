# Swagger 적용 연습 프로젝트입니다.


![](https://velog.velcdn.com/images/wodnr_09/post/7a69b133-bf54-4229-a1da-1c921c6a787d/image.png)

해당 프로젝트는 RD 레시피 저장소 프로젝트의 user app을 copy하여 일부 변경한 프로젝트입니다.

[개인 블로그 참조](https://velog.io/@wodnr_09/Swagger%EC%A0%81%EC%9A%A9)

---

### 실행 가이드

**Requirements**
```
Install Python3.8

$ python3 -m venv ./{your venv name}    가상환경 생성
$ source {your venv name}/bin/activate  가상환경 실행
```
**Installation**
```
$ git clone https://github.com/wodnrP/Swagger_practise.git
$ pip install -r requirements.txt       프로젝트 패키지 설치 
```

**.env file create**
- 프로젝트 폴더와 같은 위치에 .env file 생성
- https://djecrety.ir/ 에서 django secret_key 생성 후 .env file에 작성
```
DEBUG=...   
SECRET_KEY=...
```

**static setting**
- 프로젝트 폴더와 같은 위치에 static 디렉토리 생성
- static 디렉토리 하위에 css, image, js 디렉토리 생성
- 이후 다음과 같은 코드 실행
```
$ python3 manage.py collectstatic
```

**Migration**
```
$ python3 manage.py makemigrations
$ python3 manage.py migrate
```

**RUN**
```
$ python3 manage.py runserver
```

- `/swagger` 를 통해 Swagger UI 확인  
