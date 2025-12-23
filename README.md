# 삼천리 경영지표 관리 시스템 (Business Index Management System)

삼천리 경영지표 관리 시스템은 법인별/사업영역별 일일 경영 지표를 입력하고 관리할 수 있는 웹 기반 플랫폼입니다.

## 🚀 주요 기능

### 1. 인증 및 권한 관리
*   **보안 로그인**: Django 표준 인증 시스템을 기반으로 한 안전한 로그인 기능.
*   **동적 메뉴 권한**: 관리자가 사용자별로 접근 가능한 사업영역(FO, BM, EV 등) 메뉴를 지정할 수 있습니다.
*   **메뉴 필터링**: 로그인 시 사용자가 권한을 가진 메뉴만 사이드바에 노출되며, 권한이 없는 경우 안내 페이지로 라우팅됩니다.

### 2. 지표 실적 관리
*   **사업영역별 입력**: FO(미주), BM(모터스), EV 등 각 사업영역별 전용 입력 페이지를 제공합니다.
*   **계층형 지표 구조**: 대분류(CategoryGroup) > 소분류(Category) > 지표항목(Indicator)으로 구성된 체계적인 마스터 관리를 지원합니다.
*   **일일 실적 입력**: 날짜별로 지표 실적을 편리하게 입력하고 수정할 수 있는 테이블 UI를 제공합니다.
*   **데이터 병합 표시**: 대분류와 소분류 항목에 Rowspan을 적용하여 시각적으로 가독성 높은 표를 제공합니다.

### 3. 사용자 및 시스템 관리
*   **사용자 현황**: 현재 등록된 사용자 목록과 각 사용자의 이메일, 부여된 메뉴 권한을 한눈에 조회합니다.
*   **직관적인 권한 설정**: 별도의 관리자 페이지 이동 없이 메인 UI에서 모달을 통해 즉시 메뉴 권한을 부여하거나 회수할 수 있습니다.
*   **Django Admin 연동**: 지표 마스터 데이터 및 상세 데이터 관리를 위한 강력한 백엔드 인터페이스를 제공합니다.

## 🛠 기술 스택

*   **Backend**: Python 3.12, Django 5.0
*   **Database**: PostgreSQL
*   **Frontend**: HTML5, Vanilla JavaScript, Tailwind CSS (CDN), jQuery (DataTables 활용)
*   **Infrastructure**: Docker, Docker Compose

## 📦 설치 및 실행 방법

### 1. 환경 설정 (.env)
프로젝트 루트 폴더에 `.env` 파일을 생성하고 다음 내용을 설정합니다.
```env
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=postgres://postgres:postgres@db:5432/business_index
ALLOWED_HOSTS=*
```

### 2. 컨테이너 실행
Docker가 설치된 환경에서 다음 명령어를 실행합니다.
```bash
docker-compose up -d --build
```

### 3. 초기 데이터 세팅 (마이그레이션)
```bash
docker-compose exec web python manage.py migrate
```

## 📂 프로젝트 구조

*   `accounts/`: 사용자 인증 및 계정 관리 관련 로직
*   `dashboard/`: 지표 관리, 실적 입력, 사용자 권한 관리 핵심 로직
*   `config/`: Django 프로젝트 설정 (Settings, URLs)
*   `templates/`: 전역 base 레이아웃 및 공통 템플릿
*   `static/`: 이미지 및 정적 리소스 파일
