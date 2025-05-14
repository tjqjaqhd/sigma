# 사양서(명세서) - simulator 모듈

## 1. 목적 및 개요
- 전략-실행기-피드백-성과분석을 하나의 시뮬레이션 루프로 통합

## 2. 함수/입출력/예외
- run_simulation(strategy_func, data_stream, mode, initial_balance, fee):
    - 입력: 전략 함수, 데이터 스트림, 모드, 시작 잔고, 수수료
    - 출력: {'results', 'performance', 'final_balance', 'trades', 'return'}
    - 예외: 각 단계별 에러는 handle_error로 일원화
- 공통 예외: 모든 함수는 handle_error로 예외 일원화

## 3. 테스트/확장성
- __main__ 예시 및 실제 실행 결과, 모든 테스트 통과
- 멀티 전략, 병렬 실행 등 함수 추가만으로 구조 유지

## 4. 참고사항
- 실시간 연동, 가상 데이터 생성 등 확장 가능
- **차익거래 전략도 반드시 시뮬레이터에서 실험/검증 후 실전 적용**
- **시뮬레이터는 실전과 동일한 전략 함수와 직접 연동되어야 하며, 모의투자(실험)용임을 명확히 함**
- 전략 신호 함수(`arbitrage_signal_strategy`)는 별도 파일(`arbitrage_signal.py`)에 정의되어 있으며, 시뮬레이터에서는 import 하여 사용합니다.
- 예시: `from src.strategy.arbitrage_signal import arbitrage_signal_strategy` 