# Swagger 적용 연습 프로젝트입니다.


![](https://velog.velcdn.com/images/wodnr_09/post/7a69b133-bf54-4229-a1da-1c921c6a787d/image.png)

해당 프로젝트는 RD 레시피 저장소 프로젝트의 user app을 copy하여 일부 변경한 프로젝트입니다.

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
```
DEBUG=...   
SECRET_KEY=...
```
https://djecrety.ir/ 에서 django secret_key 생성 후 .env file에 작성

**Migration**
```
$ python3 manage.py makemigrations
$ python3 manage.py migrate
```

**RUN**
```
$ python3 manage.py runserver
```

`/swagger` 를 통해 Swagger UI 확인  
