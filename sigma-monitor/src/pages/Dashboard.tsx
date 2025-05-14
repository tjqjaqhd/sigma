import React, { useEffect, useState } from 'react'
import { Box, Typography, Grid, Paper, Button } from '@mui/material'
import { useStrategyStore } from '../store/strategy/strategyStore.ts'
import { api } from '../api/client.ts'

/**
 * 대시보드 페이지 컴포넌트
 * 시스템의 주요 정보와 상태를 보여줍니다
 */

// 목업 전략 목록
const mockStrategies = [
  { id: '1', name: '전략A', status: 'running', pnl: 10000 },
  { id: '2', name: '전략B', status: 'stopped', pnl: -5000 }
]
// 목업 로그
const mockLogs = [
  { id: '1', timestamp: '2024-06-01 12:00', level: 'info', message: '전략A 시작' }
]

const Dashboard = () => {
  // 버전 정보(실제 API 연동)
  const [version, setVersion] = useState('로딩중...')
  useEffect(() => {
    api.system.getMetrics().then(res => {
      setVersion((res.data.data as any)?.version || '알 수 없음')
    }).catch(() => setVersion('연결 실패'))
  }, [])

  // 전략 시작/정지(실제 연동)
  const { startStrategy, stopStrategy, isLoading } = useStrategyStore()
  // 전략 목록/로그(목업)
  const strategies = mockStrategies
  const logs = mockLogs

  return (
    <Box>
      <Typography variant="h4" gutterBottom>대시보드</Typography>
      <Paper sx={{ p: 2, mb: 2 }}>
        <Typography variant="h6">버전 업데이트</Typography>
        <Typography>현재 버전: {version}</Typography>
      </Paper>
      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6">전략 목록</Typography>
            {strategies.map(s => (
              <Box key={s.id} sx={{ mb: 1 }}>
                <Typography>{s.name} ({s.status})</Typography>
                <Button
                  variant="contained"
                  color={s.status === 'running' ? 'error' : 'primary'}
                  onClick={() =>
                    s.status === 'running'
                      ? stopStrategy(s.id)
                      : startStrategy(s.id)
                  }
                  disabled={isLoading}
                >
                  {s.status === 'running' ? '정지' : '시작'}
                </Button>
              </Box>
            ))}
          </Paper>
        </Grid>
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6">최근 로그</Typography>
            {logs.map(l => (
              <Typography key={l.id}>{l.timestamp} - {l.message}</Typography>
            ))}
          </Paper>
        </Grid>
      </Grid>
    </Box>
  )
}

export default Dashboard 