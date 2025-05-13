import create from 'zustand';
import { api } from '../../api/client.ts';
import type { Strategy } from '../../types';

interface StrategyState {
  strategies: Strategy[];
  isLoading: boolean;
  error: string | null;
  selectedStrategyId: string | null;
  
  // 액션
  fetchStrategies: () => Promise<void>;
  startStrategy: (id: string) => Promise<void>;
  stopStrategy: (id: string) => Promise<void>;
  updateParameters: (id: string, parameters: Record<string, any>) => Promise<void>;
  selectStrategy: (id: string) => void;
}

export const useStrategyStore = create<StrategyState>((set, get) => ({
  strategies: [],
  isLoading: false,
  error: null,
  selectedStrategyId: null,

  fetchStrategies: async () => {
    set({ isLoading: true });
    try {
      const response = await api.strategy.getStatus();
      set({ strategies: response.data.data, error: null });
    } catch (error) {
      set({ error: (error as Error).message });
    } finally {
      set({ isLoading: false });
    }
  },

  startStrategy: async (id: string) => {
    set({ isLoading: true });
    try {
      await api.strategy.start(id);
      await get().fetchStrategies();
    } catch (error) {
      set({ error: (error as Error).message });
    } finally {
      set({ isLoading: false });
    }
  },

  stopStrategy: async (id: string) => {
    set({ isLoading: true });
    try {
      await api.strategy.stop(id);
      await get().fetchStrategies();
    } catch (error) {
      set({ error: (error as Error).message });
    } finally {
      set({ isLoading: false });
    }
  },

  updateParameters: async (id: string, parameters: Record<string, any>) => {
    set({ isLoading: true });
    try {
      await api.strategy.updateParameters(id, parameters);
      await get().fetchStrategies();
    } catch (error) {
      set({ error: (error as Error).message });
    } finally {
      set({ isLoading: false });
    }
  },

  selectStrategy: (id: string) => {
    set({ selectedStrategyId: id });
  },
})); 