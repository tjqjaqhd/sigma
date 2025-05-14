# SIGMA 자동화 트레이딩 시스템

## 폴더 구조

- src/
  - data/           # 데이터 수집, 전처리, DB 등
  - event/          # 이벤트 감지
  - strategy/       # 전략 엔진, 피드백, 모니터링 등
  - execution/      # 주문 실행
  - dashboard/      # 대시보드(웹앱)
  - utils/          # 공통유틸(설정, 로깅, 에러처리 등)
- tests/            # 테스트 코드

## 공통유틸(utils) 설명
- config.py: 시스템 환경설정/변수 관리
- logger.py: 실행/에러/이벤트 로깅
- error_handling.py: 공통 예외/에러 처리
- 각 모듈은 사양서(.md)와 코드(.py)가 1:1로 관리됨
