// 전략 관련 타입
export interface Strategy {
  id: string;
  name: string;
  status: 'running' | 'stopped' | 'error';
  pnl: number;
  parameters: Record<string, any>;
  lastUpdate: string;
}

// 로그 관련 타입
export interface Log {
  id: string;
  timestamp: string;
  level: 'info' | 'warning' | 'error';
  message: string;
  strategyId?: string;
}

// 시스템 상태 타입
export interface SystemMetrics {
  cpu: number;
  memory: number;
  disk: number;
  connections: {
    redis: boolean;
    database: boolean;
    api: boolean;
  };
}

// API 응답 타입
export interface ApiResponse<T> {
  success: boolean;
  data: T;
  error?: string;
}

// 웹소켓 메시지 타입
export interface WebSocketMessage {
  type: 'strategy' | 'log' | 'system';
  data: any;
  timestamp: string;
} 