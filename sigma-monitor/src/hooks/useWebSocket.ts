import { useEffect, useRef, useCallback } from 'react';
import type { WebSocketMessage } from '../types';

interface WebSocketOptions {
  url: string;
  onMessage: (data: WebSocketMessage) => void;
  onError?: (error: Event) => void;
  reconnectInterval?: number;
  maxRetries?: number;
}

export const useWebSocket = ({
  url,
  onMessage,
  onError,
  reconnectInterval = 3000,
  maxRetries = 5,
}: WebSocketOptions) => {
  const ws = useRef<WebSocket | null>(null);
  const retries = useRef(0);

  const connect = useCallback(() => {
    try {
      ws.current = new WebSocket(url);

      ws.current.onmessage = (event) => {
        const data = JSON.parse(event.data) as WebSocketMessage;
        onMessage(data);
      };

      ws.current.onerror = (error) => {
        onError?.(error);
      };

      ws.current.onclose = () => {
        if (retries.current < maxRetries) {
          retries.current += 1;
          setTimeout(connect, reconnectInterval);
        }
      };

      ws.current.onopen = () => {
        retries.current = 0;
      };
    } catch (error) {
      onError?.(error as Event);
    }
  }, [url, onMessage, onError, reconnectInterval, maxRetries]);

  useEffect(() => {
    connect();
    return () => {
      if (ws.current) {
        ws.current.close();
      }
    };
  }, [connect]);

  const sendMessage = useCallback((message: any) => {
    if (ws.current?.readyState === WebSocket.OPEN) {
      ws.current.send(JSON.stringify(message));
    }
  }, []);

  return {
    sendMessage,
    isConnected: ws.current?.readyState === WebSocket.OPEN,
  };
}; 