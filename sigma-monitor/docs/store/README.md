# 상태 관리 사양서

## 스토어 구조
```
store/
├── strategy/     # 전략 상태 관리
├── system/       # 시스템 상태 관리
└── logs/         # 로그 상태 관리
```

## 1. 전략 상태 (strategy)
```typescript
interface StrategyState {
  strategies: {
    [id: string]: {
      status: 'running' | 'stopped' | 'error';
      pnl: number;
      parameters: Record<string, any>;
      priority: number;
      lastUpdate: string;
    }
  };
  isLoading: boolean;
  error: string | null;
}

// 액션
const actions = {
  startStrategy: (id: string) => void;
  stopStrategy: (id: string) => void;
  updateParameters: (id: string, params: object) => void;
  setPriority: (id: string, priority: number) => void;
}
```

## 2. 시스템 상태 (system)
```typescript
interface SystemState {
  resources: {
    cpu: number;
    memory: number;
    disk: number;
  };
  connections: {
    redis: boolean;
    database: boolean;
    api: boolean;
  };
  alerts: Array<{
    id: string;
    type: 'warning' | 'error';
    message: string;
    timestamp: string;
  }>;
}
```

## 3. 로그 상태 (logs)
```typescript
interface LogState {
  entries: Array<{
    id: string;
    strategy: string;
    level: 'info' | 'warning' | 'error';
    message: string;
    timestamp: string;
  }>;
  filter: {
    strategy: string | null;
    level: string | null;
    search: string;
  };
  isStreaming: boolean;
}
```

## 상태 관리 규칙
1. 불변성 유지
2. 액션 타입 상수 정의
3. 선택자(selector) 사용
4. 비동기 액션 처리
5. 상태 지속성 관리 