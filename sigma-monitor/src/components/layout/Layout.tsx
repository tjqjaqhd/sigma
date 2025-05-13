import React from 'react';
import { Box, CssBaseline } from '@mui/material';
import Header from './Header.tsx';
import Sidebar from './Sidebar.tsx';

interface LayoutProps {
  children: React.ReactNode;
}

/**
 * 앱의 기본 레이아웃을 정의하는 컴포넌트
 * @param {LayoutProps} props - 레이아웃에 표시될 자식 컴포넌트
 * @returns {JSX.Element} 레이아웃 컴포넌트
 */
const Layout: React.FC<LayoutProps> = ({ children }) => {
  const [sidebarOpen, setSidebarOpen] = React.useState(true);

  const handleSidebarToggle = () => {
    setSidebarOpen(!sidebarOpen);
  };

  return (
    <Box sx={{ display: 'flex', minHeight: '100vh' }}>
      <CssBaseline />
      <Header onSidebarToggle={handleSidebarToggle} />
      <Sidebar open={sidebarOpen} onClose={() => setSidebarOpen(false)} />
      <Box
        component="main"
        sx={{
          flexGrow: 1,
          p: 3,
          width: { sm: `calc(100% - ${240}px)` },
          ml: { sm: `${240}px` },
          mt: '64px'
        }}
      >
        {children}
      </Box>
    </Box>
  );
};

export default Layout; 