# 컴포넌트 사양서

## 컴포넌트 구조
```
components/
├── common/       # 공통 컴포넌트
├── strategy/     # 전략 관련 컴포넌트
├── logs/         # 로그 관련 컴포넌트
└── system/       # 시스템 상태 컴포넌트
```

## 1. 공통 컴포넌트 (common)
- **Button**: 시작/정지/설정 등 공통 버튼
- **Card**: 전략/로그 표시용 카드
- **Table**: 데이터 테이블
- **Chart**: 차트 컴포넌트
- **Alert**: 알림 메시지

## 2. 전략 컴포넌트 (strategy)
- **StrategyCard**: 개별 전략 카드
- **StrategyControls**: 전략 제어 버튼
- **ParameterEditor**: 파라미터 수정
- **PrioritySlider**: 우선순위 조절

## 3. 로그 컴포넌트 (logs)
- **LogStream**: 실시간 로그 표시
- **LogFilter**: 로그 필터링
- **LogSearch**: 로그 검색
- **LogLevel**: 로그 레벨 표시

## 4. 시스템 컴포넌트 (system)
- **ResourceMonitor**: CPU/RAM 모니터
- **ConnectionStatus**: 연결 상태
- **SystemAlert**: 시스템 알림
- **MetricsGraph**: 시스템 메트릭 그래프

## 컴포넌트 공통 규칙
1. TypeScript 사용 필수
2. Props 인터페이스 정의
3. 스타일은 styled-components 사용
4. 에러 처리 포함 