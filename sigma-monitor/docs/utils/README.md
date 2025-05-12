# 유틸리티 사양서

## 유틸리티 함수 목록

### 1. 날짜/시간 처리
```typescript
// 타임스탬프 포맷
formatTimestamp(date: Date): string

// 시간 간격 계산
getTimeInterval(start: Date, end: Date): string

// 거래 시간대 체크
isMarketHours(timestamp: Date): boolean
```

### 2. 수치 계산/포맷
```typescript
// 수익률 계산
calculatePnL(entry: number, current: number): number

// 숫자 포맷 (천단위 콤마, 소수점)
formatNumber(value: number, decimals?: number): string

// 퍼센트 변환
toPercentage(value: number): string
```

### 3. 데이터 변환
```typescript
// CSV 변환
exportToCsv(data: any[]): string

// JSON 정규화
normalizeData(data: any): object

// 차트 데이터 포맷
formatChartData(data: any[]): ChartData
```

### 4. 검증/필터
```typescript
// 파라미터 검증
validateParameters(params: object, schema: object): boolean

// 로그 레벨 필터
filterLogsByLevel(logs: Log[], level: string): Log[]

// 전략 ID 검증
isValidStrategyId(id: string): boolean
```

### 5. 에러 처리
```typescript
// 에러 래핑
wrapError(error: Error): AppError

// API 에러 처리
handleApiError(error: Error): void

// 재시도 로직
retry<T>(fn: () => Promise<T>, attempts: number): Promise<T>
```

## 유틸리티 사용 규칙
1. 순수 함수로 구현
2. 타입 정의 필수
3. 에러 처리 포함
4. 단위 테스트 작성 