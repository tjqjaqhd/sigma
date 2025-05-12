# API 연동 사양서

## API 구조
```
api/
├── endpoints/    # REST API 엔드포인트
└── websocket/    # WebSocket 연결
```

## 1. REST API 엔드포인트
### 전략 제어
```typescript
// 전략 시작
POST /api/strategy/start
{
  "strategy_id": string,
  "parameters": object
}

// 전략 중지
POST /api/strategy/stop
{
  "strategy_id": string
}

// 전략 상태 조회
GET /api/strategy/status
Response: {
  "strategies": [
    {
      "id": string,
      "status": "running" | "stopped" | "error",
      "pnl": number,
      "last_update": string
    }
  ]
}
```

### 시스템 상태
```typescript
// 시스템 메트릭
GET /api/system/metrics
Response: {
  "cpu": number,
  "memory": number,
  "disk": number,
  "connections": {
    "redis": boolean,
    "database": boolean
  }
}
```

## 2. WebSocket 연동
### 연결 설정
```typescript
const ws = new WebSocket('ws://api/stream')
```

### 구독 토픽
1. **로그 스트림**
   ```typescript
   {
     "type": "subscribe",
     "channel": "logs",
     "filter": {
       "strategy": string,
       "level": "info" | "warning" | "error"
     }
   }
   ```

2. **전략 업데이트**
   ```typescript
   {
     "type": "subscribe",
     "channel": "strategy_updates",
     "strategy_id": string
   }
   ```

### 에러 처리
- 연결 재시도: 3초 간격, 최대 5회
- 자동 재연결 구현
- 하트비트 체크: 30초 간격 