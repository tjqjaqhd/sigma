# Header
## 버전
v0.1.0

## 설명
앱 상단의 고정 헤더 컴포넌트입니다.  
사이드바 토글 버튼과 타이틀(시그마 모니터)을 표시합니다.

## 인터페이스
```ts
interface HeaderProps {
  onSidebarToggle: () => void
}
```
- props: onSidebarToggle(사이드바 열기/닫기 핸들러)
- 내부 상태: 없음

## 의존성
- @mui/material (AppBar, Toolbar, IconButton 등)
- @mui/icons-material (MenuIcon)
- React

## 사용법
```tsx
<Header onSidebarToggle={handleSidebarToggle} />
```
- Layout 등에서 사용

## 변경 이력
- 0.1.0: 최초 작성 