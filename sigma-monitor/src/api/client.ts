import axios from 'axios';
import type { Strategy, SystemMetrics, ApiResponse, Log } from '../types';

const BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export const apiClient = axios.create({
  baseURL: BASE_URL,
  timeout: 5000,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const api = {
  strategy: {
    start: (id: string) => 
      apiClient.post<ApiResponse<void>>(`/strategy/${id}/start`),
    
    stop: (id: string) => 
      apiClient.post<ApiResponse<void>>(`/strategy/${id}/stop`),
    
    getStatus: () => 
      apiClient.get<ApiResponse<Strategy[]>>('/strategy/status'),
    
    updateParameters: (id: string, parameters: Record<string, any>) =>
      apiClient.put<ApiResponse<void>>(`/strategy/${id}/parameters`, { parameters }),
  },

  system: {
    getMetrics: () => 
      apiClient.get<ApiResponse<SystemMetrics>>('/system/metrics'),
  },

  logs: {
    getRecent: (limit: number = 100) =>
      apiClient.get<ApiResponse<Log[]>>('/logs/recent', { params: { limit } }),
    
    getByStrategy: (strategyId: string, limit: number = 100) =>
      apiClient.get<ApiResponse<Log[]>>(`/logs/strategy/${strategyId}`, { 
        params: { limit } 
      }),
  },
}; 