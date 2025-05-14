# SIGMA 구현 명세 – 2단계: 실행기 (확정 버전)

이 문서는 SIGMA 자동매매 시스템의 2단계 구현 작업인 **전략 실행기(executor) 계층**의 목표, 구조, 함수 명세, 예외처리, 확장성 기준을 확정한다.

## 목표
- 바이낸스(현물, 1배 공매도, 차익거래) 전략 실행을 위한 주문 처리
- 실거래/시뮬레이션/백테스트 모드 분리 및 확장성 확보
- 실행 결과를 포트폴리오/상태에 반영
- 예외/에러 상황에 대한 명확한 처리 및 로깅

---

## 작업 체크리스트

### 1. 전략 실행 함수 (`execute_order`)
- [x] 입력: 전략 dict (예: {'symbol': 'BTCUSDT', 'action': 'sell', 'amount': 0.1, 'type': 'spot'/'margin'/'arbitrage'})
- [x] mode 파라미터: 'simulation', 'live', 'backtest' 지원
- [x] 'simulation' 모드: 임의 체결 결과 dict 반환 (예: {'status': 'simulated', ...})
- [x] 'live' 모드: 바이낸스 API 주문 실행 (실제 POST, 테스트넷/주석 처리 가능)
- [x] 'backtest' 모드: 과거 데이터 기반 체결 시뮬레이션
- [x] 실패/예외 시 명확한 에러 메시지와 실패 dict 반환 (예: {'status': 'failed', 'reason': ...})
- [x] 모든 예외/에러는 utils/error_handling.handle_error로 로깅

### 2. 포트폴리오/상태 반영 함수 (`update_portfolio`)
- [x] 입력: 실행 결과 dict
- [x] 상태 저장소(메모리/SQLite/Redis 등) 선택 저장 (현재 메모리)
- [x] 단순 출력(log)부터 시작, 확장 시 DB 연동
- [x] 실패/에러 시 예외 메시지/로깅

### 3. 실행기 내부 분기/확장 구조
- [x] mode 분기 구조 명확히 정의 ('simulation', 'live', 'backtest')
- [x] 거래소/주문 타입(spot, margin, arbitrage)별로 함수 분리/확장 가능하게 설계
- [x] 실전/모의/백테스트 로직이 명확히 분리되도록 처리

### 4. 예외/에러 처리
- [x] 모든 함수에 try-except 적용, 에러 발생 시 utils/error_handling.handle_error로 로깅
- [x] API rate limit, 주문 실패, 데이터 누락 등 상황별 예외 메시지 명확화

### 5. 테스트/검증 기준
- [x] 각 모드별(시뮬레이션/실거래/백테스트) 최소 1회 실행 테스트
- [x] 입력/출력 예시, 실패 케이스, 에러 로그 확인

---

## 구현/테스트 결과 요약

- **execute_order**
  - 시뮬레이션/백테스트/실거래(live) 모드별 정상 동작 확인
  - 실패 케이스: 필수 필드 누락, 잘못된 mode 등은 status='failed', reason에 상세 메시지 반환
  - 에러 발생 시 handle_error로 일원화 로깅
- **update_portfolio**
  - 주문 결과에 따라 메모리상 포트폴리오 정상 업데이트 및 로그 출력
- **테스트 결과**
  - tests/test_executor.py에서 각 모드별 자동 테스트 통과
  - 실거래(live)는 주석 해제 시 실제 주문 발생(주의)

## 구현 완료 기준
- src/execution/executor.py에 execute_order, update_portfolio 함수가 명세대로 구현되어야 함
- mode별로 정상 동작 및 예외/에러 상황이 모두 테스트/로깅되어야 함
- 확장(새 거래소/주문 방식 등) 시 함수 추가만으로 구조가 유지되어야 함
- 모든 함수/로직은 문서와 1:1로 동기화되어야 함