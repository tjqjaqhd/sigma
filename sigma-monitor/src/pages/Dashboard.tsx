import React from 'react';
import { Box, Typography, Grid, Paper } from '@mui/material';

/**
 * 대시보드 페이지 컴포넌트
 * 시스템의 주요 정보와 상태를 보여줍니다
 */
const Dashboard = () => {
  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        대시보드
      </Typography>
      <Grid container spacing={3}>
        <Grid item xs={12} md={6} lg={4}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6">시스템 상태</Typography>
            {/* 여기에 시스템 상태 정보가 들어갈 예정 */}
          </Paper>
        </Grid>
        <Grid item xs={12} md={6} lg={4}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6">실행 중인 전략</Typography>
            {/* 여기에 전략 목록이 들어갈 예정 */}
          </Paper>
        </Grid>
        <Grid item xs={12} md={6} lg={4}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6">최근 로그</Typography>
            {/* 여기에 최근 로그가 들어갈 예정 */}
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Dashboard; 