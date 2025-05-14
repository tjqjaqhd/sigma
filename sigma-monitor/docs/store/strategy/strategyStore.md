# strategyStore
## 버전
v0.1.0

## 설명
전략 목록, 상태, 선택, 실행/정지/파라미터 변경 등 전략 관련 상태 관리를 담당하는 zustand 기반 스토어입니다.

## 인터페이스
```ts
interface StrategyState {
  strategies: Strategy[]
  isLoading: boolean
  error: string | null
  selectedStrategyId: string | null
  fetchStrategies: () => Promise<void>
  startStrategy: (id: string) => Promise<void>
  stopStrategy: (id: string) => Promise<void>
  updateParameters: (id: string, parameters: Record<string, any>) => Promise<void>
  selectStrategy: (id: string) => void
}
```

## 의존성
- zustand
- api (client)
- types (Strategy)

## 사용법
```ts
const { strategies, fetchStrategies, startStrategy } = useStrategyStore()
```

## 변경 이력
- 0.1.0: 최초 작성 