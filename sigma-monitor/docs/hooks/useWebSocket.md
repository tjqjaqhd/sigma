# useWebSocket
## 버전
v0.1.0

## 설명
웹소켓 연결 및 메시지 수신, 재연결, 전송 기능을 제공하는 커스텀 훅입니다.

## 인터페이스
```ts
interface WebSocketOptions {
  url: string
  onMessage: (data: WebSocketMessage) => void
  onError?: (error: Event) => void
  reconnectInterval?: number
  maxRetries?: number
}
```
- 반환값: { sendMessage, isConnected }

## 의존성
- React (useEffect, useRef, useCallback)
- types (WebSocketMessage)

## 사용법
```ts
const { sendMessage, isConnected } = useWebSocket({ url, onMessage })
```

## 변경 이력
- 0.1.0: 최초 작성 