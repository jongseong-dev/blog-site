# blog-site

- "예제로 배우는 Django 4" 책을 보고 만든 예제 Repo

<!-- TOC -->

* [blog-site](#blog-site)
* [프로젝트 시작하기](#프로젝트-시작하기)
    * [필요한 요소 세팅 및 Django App 실행하기](#필요한-요소-세팅-및-django-app-실행하기)
        * [1. 패키지 설치](#1-패키지-설치)
        * [2. DB 설치 후 migration](#2-db-설치-후-migration)
        * [3. Django 실행하기](#3-django-실행하기)
        * [4. Django test 실행하기](#4-django-test-실행하기)
    * [번외. docker-compose로 실행하기](#번외-docker-compose로-실행하기)
        * [1. docker-compose 서비스 실행](#1-docker-compose-서비스-실행)
        * [2. docker-compose 서비스 종료](#2-docker-compose-서비스-종료)
    * [환경변수](#환경변수)
        * [Django Config](#django-config)
        * [DB](#db)
        * [EMAIL](#email)
* [프로젝트의 기능 소개](#프로젝트의-기능-소개)
* [CI](#ci)

<!-- TOC -->

# 프로젝트 시작하기

## 필요한 요소 세팅 및 Django App 실행하기

- 들어가기에 앞서 `poetry`와 `docker`를 설치해주세요.
    - poetry 설치 방법: https://python-poetry.org/docs/#installation
    - docker 설치 방법: https://docs.docker.com/engine/install/

- DJANGO_SETTING_MODULE 설정하기
    - 현재 개발환경에서는 `config.settings.local`을 사용하고 있습니다.
    - 따라서 명령마다 --settings 옵션을 넣기 불편하다면 **DJANGO_SETTING_MODULE**을 `config.settings.local`로 설정해주세요.

### 1. 패키지 설치

- poetry를 통해 패키지를 설치합니다.

  ```bash
  poetry install
  ```

- 가상환경이 활성화 되었다면 `pre-commit`을 설치합니다.

  ```bash
  pre-commit install
  ```

### 2. DB 설치 후 migration

- django를 띄우기 위해 db를 설치합니다.
  ```bash
  docker-compose up -d db
  ```

- 해당 db가 무사히 실행되었다면, migration을 실행합니다.
- 이떄 주의할 점은 project 위치는 webapp 이므로 `webapp`으로 이동 후 실행합니다.
  ```bash 
  python manage.py migrate --settings=config.settings.local
  ```

### 3. Django 실행하기

- migration이 완료되었다면, django를 실행합니다.

  ```bash
  python manage.py runserver --settings=config.settings.local
  ```

### 4. Django test 실행하기

- test는 아래와 같이 실행합니다.

- Linux, MacOS
  ```bash
  pytest
  ```

- 만약 test 가 제대로 실행되지 않는다면 pytest의 실행 위치가 `webapp` 디렉토리인지 확인해주세요.

## 번외. docker-compose로 실행하기

- 만약 docker-compose를 통해 Django를 실행시키고 싶다면 steps를 따라주세요.

### 1. docker-compose 서비스 실행

- docker compose 를 통해 db와 test, was를 실행합니다.

  ```bash
  docker-compose up --build -d db
  docker-compose up --build web 
  docker-compose up --build test_web 
  ```

### 2. docker-compose 서비스 종료

- 확인했다면 docker-compose에 떠있는 container를 종료시킵니다.

  ```bash
  docker-compose down
  ```

## 환경변수

- 기본값이 없는 경우 **직접 지정해야 합니다.**

### Django Config

| 변수명                    | 기본값            | 비고                                                      |
|------------------------|----------------|---------------------------------------------------------| 
| DJANGO_SETTINGS_MODULE | 없음             |                                                         |
| SECRET_KEY             | 94n7fx27pd-... | local 환경과 test 환경에서는 기본값을 사용하지만 <br/> prod에서는 주입해야 합니다. |

### DB

| 변수명         | 기본값       |
|-------------|-----------|
| DB_NAME     | postgres  |
| DB_USER     | postgres  |
| DB_PASSWORD | postgres  |
| DB_HOST     | localhost |
| DB_PORT     | 5432      |

### EMAIL

| 변수명                 | 기본값                   |
|---------------------|-----------------------|
| EMAIL_HOST_PASSWORD | 없음                    |
| EMAIL_HOST          | smtp.gmail.com        |
| EMAIL_HOST_USER     | dlwhdtjd098@gmail.com |
| EMAIL_PORT          | 587                   |
| EMAIL_USE_TLS       | True                  |

# 프로젝트의 기능 소개

- 게시물 작성하기
- 게시물 조회하기
- 게시물 이메일로 공유하기
- 게시물 태깅하기
- 게시물 피드
    - 신디케이션 피드 프레임워크 사용
    - 새로운 콘텐츠의 알림을 받는 피드 수집기를 사용해서 피드를 구독할 수 있음
- 전문(FULL-TEXT)검색 기능
    - Postgres의 Full-Text 검색 기능을 사용
    - 복잡한 검색을 수행하는 경우 유사성을 기준으로 결과를 검색
    - 텍스트에 나타나는 빈도 또는 서로 다른 필드의 중요도에 따라 용어에 가중치를 지정
    - **형태소 분석**
        - 검색 엔진에서 색인된 단어를 해당 어간으로 줄이고 변화된 단어나 파생된 단어로 매칭 여부를 검사할 수 있다.
        - Django는 용어를 검색어 객체로 변환하기 위한 SearchQuery 클래스를 제공
        - 기본적으로 용어는 더 나은 일치 항목을 얻는데 도움이 되는 형태소 분석 알고리즘을 통해 전달
    - 쿼리에 가중치 부여하기
        - 검색 결과를 관련성에 따라 정렬할 때 특정 벡터의 가중치를 높일 수 있다.
    - 트라이그램 유사성 이용하여 검색기능

# CI

- 현재 github actions를 통해 docker hub로 이미지를 빌드하고 있음.
- 이미지 태그에 대한 고찰: https://jongseong-dev.github.io/today-learn/study/20240424-TL/