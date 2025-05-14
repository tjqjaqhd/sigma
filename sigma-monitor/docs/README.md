# SIGMA 모니터 구조 사양서

## 디렉토리 구조 개요
```
sigma-monitor/
├── api/          # API 통신 관련
├── components/   # 재사용 가능한 컴포넌트
├── pages/        # 페이지 컴포넌트
├── store/        # 상태 관리
├── utils/        # 유틸리티 함수
└── docs/         # 문서화
```

## 문서 구조
각 디렉토리별 상세 사양은 다음 문서들을 참조하세요:

- [페이지 구조](./pages/README.md)
- [컴포넌트 사양](./components/README.md)
- [API 연동 사양](./api/README.md)
- [상태 관리 사양](./store/README.md)
- [유틸리티 사양](./utils/README.md)

## 기술 스택
- Frontend: React + TypeScript
- 상태관리: Redux/Zustand
- API: REST + WebSocket
- UI 라이브러리: Material-UI/Ant Design 