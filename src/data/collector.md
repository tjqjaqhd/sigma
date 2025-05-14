# 사양서(명세서) - collector 모듈

## 1. 목적 및 개요
- 시장, 뉴스, 소셜, 외부 API 등 다양한 소스에서 실시간 데이터를 수집한다.

## 2. 함수/입출력/예외
- collect_market_data(top_n=10):
    - 입력: top_n
    - 출력: [{'market', 'korean_name', 'trade_price', 'acc_trade_price_24h'} ...]
    - 예외: API 실패 시 handle_error, 빈 리스트 반환
- collect_binance_spot_data(symbols=None):
    - 입력: symbols
    - 출력: [{'symbol', 'price', 'volume', 'bid', 'ask', 'timestamp'} ...]
    - 예외: API 실패 시 handle_error, 빈 리스트 반환
- collect_binance_margin_data(symbols=None):
    - 입력: symbols
    - 출력: [{'symbol', ..., 'type': 'margin'} ...]
- collect_binance_arbitrage_data():
    - 출력: [{'symbol', 'spot_price', 'margin_price', 'spread', ...}]
- run_data_pipeline(top_n=10):
    - 입력: top_n
    - 출력: 저장 성공 여부(bool)
- 공통 예외: 모든 함수는 handle_error로 예외 일원화

## 3. 테스트/확장성
- 실제 데이터 수집, 주요 필드 검증, 모든 테스트 통과
- 함수 추가만으로 구조 확장 가능

## 4. 참고사항
- 수집 주기/스케줄 관리 필요
- 피처 생성 등 확장성 고려
- **백테스트/시뮬레이션에서 과거 데이터/가상 데이터 소스로 활용 가능** 