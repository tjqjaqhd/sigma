import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Layout from './components/layout/Layout';
import Dashboard from './pages/Dashboard';

// 임시 페이지 컴포넌트들 (나중에 실제 컴포넌트로 교체될 예정)
const Strategy = () => <div>전략 관리 페이지</div>;
const Logs = () => <div>로그 조회 페이지</div>;
const Settings = () => <div>설정 페이지</div>;

/**
 * 앱의 최상위 컴포넌트
 * 라우팅 구조와 레이아웃을 정의합니다
 */
function App() {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/strategy" element={<Strategy />} />
          <Route path="/logs" element={<Logs />} />
          <Route path="/settings" element={<Settings />} />
        </Routes>
      </Layout>
    </Router>
  );
}

export default App; 