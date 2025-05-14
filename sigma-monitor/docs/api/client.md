# client
## 버전
v0.1.0

## 설명
백엔드 API와 통신하는 axios 기반 클라이언트 및 API 래퍼입니다.  
전략, 시스템, 로그 관련 API를 제공합니다.

## 인터페이스
- apiClient: axios 인스턴스
- api.strategy: start, stop, getStatus, updateParameters
- api.system: getMetrics
- api.logs: getRecent, getByStrategy

## 의존성
- axios
- types(Strategy, SystemMetrics, ApiResponse, Log)

## 사용법
```ts
import { api } from '../api/client'
api.strategy.start('id')
api.system.getMetrics()
```

## 변경 이력
- 0.1.0: 최초 작성 