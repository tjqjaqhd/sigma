# SIGMA 자동화 트레이딩 시스템
## MVP 진행현황 체크리스트

---

### 1. 환경/인프라 정비
- [x] 폴더/모듈/사양서 구조 최종 점검
- [x] 공통유틸(config, logger, error_handling) 실제 동작 구현
- [x] .env, 환경변수, API키 등 설정파일 준비

### 2. 데이터 파이프라인 구현
- [x] collector: 거래소/뉴스/소셜 API 연동, 데이터 수집
- [x] preprocessor: 결측치/이상치 처리, 데이터 정규화
- [x] db: DB/캐시 연동, 데이터 저장/조회

### 3. 이벤트/트리거 감지
- [x] detector: 가격변동, 거래량 등 이벤트 감지 로직 구현

### 4. 전략 엔진 구현
- [x] gpt_controller: OpenAI API 연동, 전략 생성
- [x] local_engine: 단순/반복 전략 로직 구현

### 5. 주문/실행
- [ ] executor: 거래소 주문 API 연동, 주문/체결/실패 처리

### 5-1. 전략 검증/실험 구조 결정
- [x] 백테스트(backtest.py), 시뮬레이터(simulator.py)는 전략 레이어(src/strategy/) 내부에 위치
    - 이유: 전략 함수와의 직접 연결, 테스트/실험 자동화, 코드/사양서 동기화, 상위 설계 문서와의 일관성 유지
    - 모든 전략/이벤트/데이터 모듈은 반드시 backtest/simulator에서 직접 검증 후 실전 적용
    - 구조/위치 변경 시 반드시 architecture.md, rules.md, dev_guide.md, MVP_progress.md에 즉시 반영

### 6. 피드백/모니터링
- [ ] feedback: 주문 결과/전략 실행 결과 수집
- [ ] monitoring: 성과 분석, 로그/알림/대시보드 연동

### 7. 대시보드/알림
- [ ] dashboard: 실시간 상태/성과 시각화, 사용자 제어

### 8. 통합/테스트/배포
- [x] 각 모듈 통합, end-to-end 테스트
- [x] 샘플/실전 데이터로 전체 파이프라인 검증
- [ ] 문서(README, dev_guide, rules 등) 최종 점검
- [ ] git 커밋/푸시, 배포 스크립트 작성

---

> 각 항목을 완료할 때마다 [ ]를 [x]로 체크하며 진행상황을 관리하세요. 