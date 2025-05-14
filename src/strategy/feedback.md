# 사양서(명세서) - feedback 모듈

## 1. 모듈/기능명
feedback (피드백)

## 2. 목적 및 개요
- 전략 실행 결과를 피드백 데이터로 변환, 기록/분석에 활용

## 3. 입력/출력
- 입력: 주문 결과(dict)
- 출력: 피드백 데이터(dict, 예: {'status', 'profit', 'error', 'upbit_order', 'binance_order'})

## 4. 동작 조건 및 예외
- 데이터 누락/불일치 시 handle_error로 예외 처리

## 5. 기타 참고사항
- 피드백 데이터는 모니터링/분석 모듈과 연동됨 (analyze_performance)

## 6. 함수/입출력/예외
- collect_feedback(order_result):
    - 입력: 주문/전략 실행 결과(dict)
    - 출력: 피드백 데이터(dict)
    - 예외: 데이터 누락 등 handle_error로 처리
- save_feedback_to_file(feedback_data, filename):
    - 입력: 피드백 리스트, 파일명
    - 출력: 저장 성공 여부(bool)
    - 예외: 파일 저장 실패 등 handle_error로 처리
- 공통 예외: 모든 함수는 handle_error로 예외 일원화

## 7. 테스트/확장성
- __main__ 예시 및 실제 실행 결과, 모든 테스트 통과
- 파일/DB/클라우드 등 다양한 저장 방식으로 확장 가능 