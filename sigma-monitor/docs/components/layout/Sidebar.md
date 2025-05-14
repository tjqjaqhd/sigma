# Sidebar
## 버전
v0.1.0

## 설명
앱의 주요 네비게이션을 담당하는 사이드바 컴포넌트입니다.  
대시보드, 전략 관리, 로그 조회, 설정 등 주요 메뉴로 이동할 수 있습니다.  
모바일 환경에서는 Drawer로 동작하며, 데스크탑에서는 항상 고정됩니다.

## 인터페이스
```ts
interface SidebarProps {
  open: boolean
  onClose: () => void
}
```
- props: open(사이드바 열림 여부), onClose(닫기 핸들러)
- 내부 상태: 없음

## 의존성
- @mui/material (Drawer, List 등)
- @mui/icons-material
- react-router-dom (useNavigate, useLocation)
- React

## 사용법
```tsx
<Sidebar open={sidebarOpen} onClose={handleSidebarClose} />
```
- Layout 등에서 사용, open/onClose로 제어

## 변경 이력
- 0.1.0: 최초 작성 