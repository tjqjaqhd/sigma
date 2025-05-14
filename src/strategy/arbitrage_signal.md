# 사양서(명세서) - arbitrage_signal 모듈

## 1. 목적 및 개요
- 업비트-바이낸스 가격차 기반 차익거래 신호 전략 함수 제공

## 2. 함수/입출력/예외
- arbitrage_signal_strategy(event, context, threshold=50):
    - 입력: event(dict, 예: {'upbit_price': float, 'binance_price': float}), context(시장상황), threshold(진입 임계값, 기본 50)
    - 출력: 신호(str, '매수', '매도', '관망')
    - 예외: 가격 정보 누락 시 '관망' 반환, 기타 예외 발생 시 '관망' 반환

## 3. 반환 예시
- event = {'upbit_price': 1000, 'binance_price': 1100}, context = {}, threshold=50 → '매수'
- event = {'upbit_price': 1000, 'binance_price': 950}, context = {}, threshold=50 → '매도'
- event = {'upbit_price': 1000, 'binance_price': 1020}, context = {}, threshold=50 → '관망'

## 4. 활용 예시
- 차익거래 전략 신호 생성, 자동매매 엔진 연동, 실시간/백테스트/시뮬레이션 등에서 직접 호출

## 5. 테스트/확장성
- 다양한 가격차/임계값 조합 테스트, 신호 반환값 검증
- threshold 파라미터 조정, 추가 신호(예: 경고, 알림 등) 확장 가능 