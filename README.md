# SIGMA 자동화 트레이딩 시스템

## 폴더 구조

- src/
  - data/           # 데이터 수집, 전처리, DB 등
  - event/          # 이벤트 감지
  - strategy/       # 전략 엔진, 피드백, 모니터링, 백테스트(backtest.py), 시뮬레이션(simulator.py) 등
  - execution/      # 주문 실행
  - dashboard/      # 대시보드(웹앱)
  - utils/          # 공통유틸(설정, 로깅, 에러처리 등)
- tests/            # 테스트 코드

## 공통유틸(utils) 설명
- config.py: 시스템 환경설정/변수 관리
- logger.py: 실행/에러/이벤트 로깅
- error_handling.py: 공통 예외/에러 처리
- 각 모듈은 사양서(.md)와 코드(.py)가 1:1로 관리됨

## 전략 검증/실험
- backtest.py: 과거 데이터로 전략 성과를 검증하는 백테스트 모듈
- simulator.py: 실시간/가상 데이터로 전략을 실험하는 시뮬레이션 모듈
- 모든 전략 함수는 백테스트/시뮬레이션에서 직접 호출 가능하게 설계됨

## 운영/배포/테스트/문서화/CI/CD
- 모든 운영 환경(로컬/서버/클라우드)에서 venv 가상환경, requirements.txt로 의존성 관리
- .env 파일로 환경 변수, API 키, 보안 설정 등 관리
- pytest로 전체 파이프라인(E2E) 자동화 테스트 가능
- 배포 스크립트(deploy.sh) 및 Github Actions 등 CI/CD 자동화 도구 연동 가능(예시 제공)
- logger.py, error_handling.py를 통해 모든 예외/에러/이벤트를 로깅하며, 외부 모니터링/알림(Grafana, Slack 등) 연동 확장 가능
- 코드/문서/운영 변경 시 README, dev_guide, rules, 각 단계별 명세 등 즉시 반영(문서-코드 1:1 동기화)
- 장애/에러/운영 변경 시 즉시 대응 및 문서-코드 동기화
- 확장(새 환경/배포/모니터링/문서화 도구 등) 시 구조가 유지되도록 설계
