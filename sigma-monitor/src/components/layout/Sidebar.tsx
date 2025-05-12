import React from 'react';
import {
  Drawer,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  useTheme,
  useMediaQuery
} from '@mui/material';
import { useNavigate, useLocation } from 'react-router-dom';
import DashboardIcon from '@mui/icons-material/Dashboard';
import SettingsIcon from '@mui/icons-material/Settings';
import TimelineIcon from '@mui/icons-material/Timeline';
import StorageIcon from '@mui/icons-material/Storage';

interface SidebarProps {
  open: boolean;
  onClose: () => void;
}

/**
 * 사이드바 네비게이션 메뉴 아이템 정의
 */
const menuItems = [
  { text: '대시보드', icon: <DashboardIcon />, path: '/' },
  { text: '전략 관리', icon: <TimelineIcon />, path: '/strategy' },
  { text: '로그 조회', icon: <StorageIcon />, path: '/logs' },
  { text: '설정', icon: <SettingsIcon />, path: '/settings' }
];

/**
 * 앱의 사이드바 컴포넌트
 * @param {SidebarProps} props - 사이드바 상태 및 제어 props
 * @returns {JSX.Element} 사이드바 컴포넌트
 */
const Sidebar: React.FC<SidebarProps> = ({ open, onClose }) => {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));
  const navigate = useNavigate();
  const location = useLocation();

  const handleNavigation = (path: string) => {
    navigate(path);
    if (isMobile) {
      onClose();
    }
  };

  const drawerContent = (
    <List sx={{ width: 240, mt: '64px' }}>
      {menuItems.map((item) => (
        <ListItem
          button
          key={item.text}
          onClick={() => handleNavigation(item.path)}
          selected={location.pathname === item.path}
          sx={{
            '&.Mui-selected': {
              backgroundColor: theme.palette.action.selected
            }
          }}
        >
          <ListItemIcon sx={{ color: 'inherit' }}>
            {item.icon}
          </ListItemIcon>
          <ListItemText primary={item.text} />
        </ListItem>
      ))}
    </List>
  );

  return (
    <Drawer
      variant={isMobile ? 'temporary' : 'permanent'}
      open={open}
      onClose={onClose}
      sx={{
        '& .MuiDrawer-paper': {
          width: 240,
          boxSizing: 'border-box',
          backgroundColor: theme.palette.background.default,
          borderRight: `1px solid ${theme.palette.divider}`
        }
      }}
    >
      {drawerContent}
    </Drawer>
  );
};

export default Sidebar; 