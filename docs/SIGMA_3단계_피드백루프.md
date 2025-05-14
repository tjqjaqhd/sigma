# SIGMA 구현 명세 – 3단계: 피드백 루프 (확정 버전)

이 문서는 SIGMA 자동매매 시스템의 3단계 구현 작업인 **피드백 루프 계층**의 목표, 구조, 함수 명세, 예외처리, 확장성 기준을 확정한다.

## 목표
- 전략 실행 결과를 기록하고, 성능을 분석하여 전략 개선에 활용
- 실행 결과/이력의 저장 방식(파일, DB, 클라우드 등) 확장성 확보
- 예외/에러 상황에 대한 명확한 처리 및 로깅

---

## 작업 체크리스트

### 1. 실행 결과 기록 함수 (`feedback.py`)
- [x] collect_feedback(order_result: dict): 실행 결과를 피드백 데이터(dict)로 변환 (record_execution_result 대신)
- [x] 입력: executor에서 전달받은 실행 결과 dict
- [x] 출력: 피드백 데이터(dict, 예: {'status', 'profit', 'error', 'upbit_order', 'binance_order'})
- [x] 저장/기록은 현재 dict 변환만, 추후 콘솔/파일/DB 기록 확장 가능
- [x] 저장 실패/예외 시 handle_error로 에러 메시지/로깅
- [x] save_feedback_to_file(feedback_data, filename): 피드백 데이터 파일 저장 함수 구현

### 2. 성능 분석 함수 (`monitoring.py`)
- [x] analyze_performance(feedback_data: list) -> dict: 수익률, 성공률 등 지표 계산
- [x] 입력: 피드백 데이터 리스트
- [x] 출력: 성과 요약 dict (예: {'total_profit', 'total_trades', 'success', 'fail', 'success_rate'})
- [x] 확장: 추가 지표/분석 함수 쉽게 추가 가능하게 설계

### 3. 흐름 연동
- [x] 실행기 → collect_feedback()로 결과 전달
- [x] 피드백 데이터 리스트를 monitoring.py의 analyze_performance()에서 사용

### 4. 예외/에러 처리
- [x] 모든 함수에 try-except 적용, 에러 발생 시 utils/error_handling.handle_error로 로깅
- [x] 데이터 누락, 기록 실패 등 상황별 예외 메시지 명확화

### 5. 테스트/검증 기준
- [x] feedback.py의 __main__ 예시 등으로 기록/분석/파일저장 테스트 가능
- [x] 입력/출력 예시, 실패 케이스, 에러 로그 확인

---

## 구현/테스트 결과 요약

- **collect_feedback, analyze_performance, save_feedback_to_file**
  - 피드백 dict 변환, 성과 분석, 파일 저장 모두 정상 동작 확인
  - 실패/에러 케이스: 잘못된 입력, 파일 저장 실패 등은 handle_error로 일원화 처리
  - 확장: 파일/DB/클라우드 등 다양한 저장 방식으로 쉽게 확장 가능
- **테스트 결과**
  - __main__ 예시 및 실제 실행 결과, 모든 테스트 통과

## 구현 완료 기준
- src/strategy/feedback.py, monitoring.py에 명세대로 함수가 구현되어야 함
- 실행 결과가 정상적으로 기록/분석되고, 예외/에러 상황이 모두 테스트/로깅되어야 함
- 확장(새 지표/저장 방식 등) 시 함수 추가만으로 구조가 유지되어야 함
- 모든 함수/로직은 문서와 1:1로 동기화되어야 함