# Assingment - sehyeongkim

## Getting Started

아래 세 가지 항목이 필요합니다.
- Python 3.9.18
- pyenv : install python versions
- poetry : package manager

### Prerequisites
- FastAPI : Python Web Framework
- MySQL : Database
- sqlalchemy : DB ORM
- alembic : manage DB migrations
- uvicorn : running FastAPI worker
- docker
- docker compose

## Install packages
- 로컬 개발 환경 세팅 (가상환경 생성 및 패키지 다운로드)
```shell
pyenv local 3.9.18
poetry env use python
poetry install
```

## How to Run

### Config(Env File)
- 개발 환경에서는 dev.env.sample을 기반으로 dev.env 파일을 생성합니다.(과제 건이라 dev.env.sample 내 변수를 그대로 사용하셔도 무방합니다.)
- dev.env.sample 내 변수들은 docker-compose 사용 환경을 기반으로 작성되었습니다.

### Running
#### Local
- 데이터베이스 생성
```sql
CREATE DATABASE 44labs DEFAULT CHARACTER SET utf8 COLLATE utf8_unicode_ci;
CREATE DATABASE 44labs_test DEFAULT CHARACTER SET utf8 COLLATE utf8_unicode_ci;
```
- WAS 
```shell
alembic upgrade head
chmod +x ./app/start.sh
./app/start.sh
```

#### Docker Compose (RECOMMENDED)
```shell
docker-compose -f docker/docker-compose.yml up
```

## Tests
- 모든 기능들은 unit test와 api기반 test가 진행됩니다.
```text
tests/conftest.py 는 테스트 진행시 여러 scope를 기반으로 환경을 세팅합니다.
tests/api 디렉토리 내부엔 api 기반 test가 존재합니다.
그 외 디렉토리에서는 unit test가 진행됩니다.
```

### Config(Env File)
- docker-compose 기반으로 db 서버를 동작시켰다는 가정 하에 로컬에서 테스트코드를 작동시킬 땐, DB_HOST 설정을 localhost로 변경 후 진행합니다.

### Run Tests
```commandline
pytest tests/
```

### Test Cases
1. 회원 가입 및 로그인
   ```text
   1) POST /api/v1/signup
    - 회원가입 성공(test_signup)
    - 회원가입 필수 필드 누락(test_signup_invalid_request_required_field_not_exists)
    - 회원가입 필수 필드값 핸드폰 번호 포맷 불일치(test_signup_invalid_request_phone_number_not_valid)
    - 회원가입 필수 필드값 이메일 포맷 불일치(test_signup_invalid_request_email_not_valid)
   2) POST /api/v1/singin
    - 로그인 성공(test_signin)
    - 로그인 필수 필드값 누락(test_signin_invalid_request)
    - 로그인 필수 필드값 이메일 포맷 불일치(test_signin_invalid_request_email_not_valid)
    - 로그인 비밀번호 불일치(test_signin_invalid_request_password_does_not_match)
   ```
2. 이용자 백엔드 서비스 구현 (Admin 혹은 User Owner ONLY)
   ```text
   1) POST /api/v1/users [ADMIN ONLY]
    - 유저 생성 성공(test_create_user)
    - 유저 생성 권한 오류(test_create_user_forbidden)
    - 유저 생성 필수값 누락(test_create_user_invalid_request_required_field_not_exists)
    - 유저 생성 이메일 포맷 불일치(test_create_user_invalid_request_email_not_valid)
    - 유저 생성 핸드폰 번호 포맷 불일치(test_create_user_invalid_request_phone_not_valid)
   2) GET /api/v1/users/{user_id} [ADMIN OR OWNER ONLY]
    - 유저 정보 조회 성공(test_get_user_by_admin)
    - 유저 정보 조회 성공(test_get_user_by_owner)
    - 유저 정보 조회 권한 오류(test_get_user_owner_forbidden)
   3) GET /api/v1/users [ADMIN ONLY]
    - 유저 목록 조회 성공(test_get_users_list)
    - 유저 목록 조회 권한 오류(test_get_users_list_forbidden)
   4) PUT /api/v1/users/{user_id}
    - 유저 정보 수정 성공(test_modify_user_by_admin)
    - 유저 정보 수정 성공(test_modify_user_by_owner)
    - 유저 정보 수정 입력값 포맷 불일치(test_modify_user_invalid_request)
    - 유저 정보 수정 수정할 내용 없음(test_modify_user_empty_request)
    - 유저 정보 수정 권한 오류(test_modify_user_forbidden)
   5) DELETE /api/v1/users/{user_id} [ADMIN OR OWNER ONLY]
    - 유저 삭제 성공(test_delete_user_by_owner)
    - 유저 삭제 성공(test_delete_user_by_admin)
    - 유저 삭제 권한 오류(test_delete_forbidden)
   ```
3. 게시판 백엔드 서비스 생성
   ```text
   1) GET /api/v1/posts
    - 게시글 목록 조회 성공(test_get_posts_list)
    - 게시글 목록 조회 인증 오류(test_get_posts_list_unauthorized)
   2) POST /api/v1/posts
    - 게시글 업로드 성공(test_create_post)
    - 게시글 업로드 필수값 누락(test_create_post_invalid_request)
    - 게시글 업로드 인증 오류(test_create_post_unauthorized)
   3) GET /api/v1/posts/{post_id}
    - 게시글 조회 성공(test_get_post)
    - 게시글 조회 인증 오류(test_get_post_unauthorized)
   4) PUT /api/v1/posts/{post_id} [OWNER ONLY]
    - 게시글 수정 성공(test_modify_post)
    - 게시글 수정 허용되지 않는 범위의 데이터 수정(test_modify_post_invalid_request)
    - 게시글 수정 권한 오류(test_modify_post_forbidden)
   ```
