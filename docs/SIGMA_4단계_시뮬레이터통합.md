# SIGMA 구현 명세 – 4단계: 시뮬레이터 통합 (확정 버전)

이 문서는 SIGMA 자동매매 시스템의 4단계 구현 작업인 **시뮬레이터 통합 계층**의 목표, 구조, 함수 명세, 예외처리, 확장성 기준을 확정한다.

## 목표
- 전략 함수, 실행기, 피드백을 하나의 시뮬레이션 루프로 통합
- 실제/가상 데이터로 반복 실행 및 결과 기록/분석
- 예외/에러 상황에 대한 명확한 처리 및 로깅

---

## 작업 체크리스트

### 1. 시뮬레이션 루프 함수 (`simulator.py`)
- [x] run_simulation(strategy_func, data_stream, mode='simulation', initial_balance=1000000, fee=0.001)
- [x] 루프 내에서 전략 실행 → 주문 실행(execute_order) → 피드백 기록(collect_feedback) → 성과 분석(analyze_performance) 흐름 구현
- [x] 입력: 전략 함수, 데이터 스트림, mode, initial_balance, fee 등
- [x] 출력: 전체 실행 결과/이력 리스트(results), 성과 분석(performance), 최종 잔고(final_balance), 거래내역(trades), 수익률(return)
- [x] 확장: 멀티 전략, 병렬 실행 등 구조 확장 가능하게 설계

### 2. 흐름 연동
- [x] data/collector, preprocessor, db와 연동하여 실제/가상 데이터 공급 가능
- [x] strategy, execution, feedback, monitoring 모듈과 함수 단위로 연결

### 3. 예외/에러 처리
- [x] try-except로 각 단계별 에러 처리, utils/error_handling.handle_error로 로깅
- [x] 데이터 누락, 전략/주문 실패, 기록 실패 등 상황별 예외 메시지 명확화

### 4. 테스트/검증 기준
- [x] 샘플/실제 데이터로 최소 1회 시뮬레이션 루프 실행 테스트 가능
- [x] 입력/출력 예시, 실패 케이스, 에러 로그 확인

---

## 구현/테스트 결과 요약

- **run_simulation**
  - 전략-실행기-피드백-성과분석이 하나의 루프로 정상 동작
  - 반환값: 전체 이력(results), 성과(performance), 최종 잔고(final_balance), 거래내역(trades), 수익률(return)
  - 실패/에러 케이스: 데이터 누락, 전략/주문 실패 등은 handle_error로 일원화 처리
  - 확장: 멀티 전략, 병렬 실행 등 함수 추가만으로 구조 유지
- **테스트 결과**
  - __main__ 예시 및 실제 실행 결과, 모든 테스트 통과
  - 샘플 데이터로 최종 잔고, 거래내역, 수익률, 성과분석까지 출력 확인

## 구현 완료 기준
- src/strategy/simulator.py에 명세대로 run_simulation 함수가 구현되어야 함
- 전략-실행기-피드백이 하나의 루프로 정상 동작해야 함
- 예외/에러 상황이 모두 테스트/로깅되어야 함
- 확장(멀티 전략, 병렬 실행 등) 시 함수 추가만으로 구조가 유지되어야 함
- 모든 함수/로직은 문서와 1:1로 동기화되어야 함

```