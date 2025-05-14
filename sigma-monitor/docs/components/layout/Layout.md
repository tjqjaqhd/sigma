# Layout
## 버전
v0.1.0

## 설명
앱의 전체 레이아웃을 담당하는 컴포넌트입니다.  
Header, Sidebar, 메인 컨텐츠 영역을 포함합니다.

## 인터페이스
```ts
interface LayoutProps {
  children: React.ReactNode
}
```
- props: children(메인 컨텐츠)
- 내부 상태: sidebarOpen(사이드바 열림 여부)

## 의존성
- @mui/material (Box, CssBaseline)
- Header, Sidebar(내부 컴포넌트)
- React

## 사용법
```tsx
<Layout>
  <Dashboard />
</Layout>
```

## 변경 이력
- 0.1.0: 최초 작성 