# 사양서(명세서) - executor 모듈

## 1. 모듈/기능명
executor (전략 실행)

## 2. 목적 및 개요
- 생성된 전략에 따라 실제 주문을 실행하고, 포트폴리오 상태를 관리한다.
- **업비트 현물 매수 ↔ 바이낸스 1배 공매도(선물/마진) 차익거래**를 지원한다.

## 3. 입력/출력
- 입력: 전략, 주문 결과
- 출력: 주문 실행 결과, 포트폴리오 상태
- **차익거래 입력 예시:**
    - 거래 대상 코인, 업비트/바이낸스 가격, 주문 수량, 슬리피지/수수료 등
- **차익거래 출력 예시:**
    - 업비트 현물 매수 결과, 바이낸스 공매도 결과, 포지션/잔고 동기화, 차익 실현 여부

## 4. 동작 조건 및 예외
- 주문 실패 시 재시도/알림
- API 호출 실패 시 예외 처리
- **한쪽 거래소 주문 실패 시 전체 롤백 또는 재시도**
- **API 오류, 잔고 부족, 슬리피지 등 예외 상황 로깅/알림**

## 5. 기타 참고사항
- 거래소 API 연동, 로그 기록
- **.env 파일에 API 키/비밀키 등 민감정보 관리**
- **테스트는 mock 또는 소액 실거래로 진행 권장**

## 6. 함수/입출력/예외
- execute_order(strategy, mode='simulation'):
    - 입력: 전략 dict (예: {'symbol', 'action', 'amount', 'type'})
    - 출력: 실행 결과 dict({'status', 'order', 'reason'})
    - 예외: 필수 필드 누락, API 오류 등 handle_error로 처리
- update_portfolio(order_result):
    - 입력: 실행 결과 dict
    - 출력: 상태 저장 성공 여부(bool)
    - 예외: 입력/필수 정보 누락 등 handle_error로 처리
- execute_arbitrage(upbit_price, binance_price, amount, mode, logger):
    - 입력: 가격, 수량, 모드
    - 출력: 차익거래 결과 dict({'upbit_order', 'binance_order', 'arbitrage_profit', ...})
    - 예외: 주문 실패, API 오류 등 handle_error로 처리
- 공통 예외: 주문 실패, API 오류, 잔고 부족, 슬리피지 등 handle_error로 일원화

## 7. 테스트/확장성
- 각 모드별(시뮬/실거래/백테스트) 최소 1회 실행 테스트, 실패/에러 케이스, 에러 로그 확인
- 함수 추가만으로 구조 확장 가능 