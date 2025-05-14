import React from 'react';
import {
  AppBar,
  IconButton,
  Toolbar,
  Typography,
  useTheme
} from '@mui/material';
import MenuIcon from '@mui/icons-material/Menu';

interface HeaderProps {
  onSidebarToggle: () => void;
}

/**
 * 앱의 상단 헤더 컴포넌트
 * @param {HeaderProps} props - 사이드바 토글 핸들러
 * @returns {JSX.Element} 헤더 컴포넌트
 */
const Header: React.FC<HeaderProps> = ({ onSidebarToggle }) => {
  const theme = useTheme();

  return (
    <AppBar
      position="fixed"
      sx={{
        zIndex: theme.zIndex.drawer + 1,
        backgroundColor: theme.palette.background.paper,
        color: theme.palette.text.primary
      }}
    >
      <Toolbar>
        <IconButton
          color="inherit"
          aria-label="메뉴 열기"
          edge="start"
          onClick={onSidebarToggle}
          sx={{ mr: 2 }}
        >
          <MenuIcon />
        </IconButton>
        <Typography variant="h6" noWrap component="div">
          시그마 모니터
        </Typography>
      </Toolbar>
    </AppBar>
  );
};

export default Header; 