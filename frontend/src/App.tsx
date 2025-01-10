import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Layout } from 'antd';
import ChatInterface from './components/ChatInterface';
import DataAnalysis from './components/DataAnalysis';
import Sidebar from './components/Sidebar';
import './App.css';

const { Content, Sider } = Layout;

const App: React.FC = () => {
  return (
    <Router>
      <Layout style={{ minHeight: '100vh' }}>
        <Sider width={250} theme="light">
          <Sidebar />
        </Sider>
        <Layout>
          <Content style={{ margin: '24px 16px', padding: 24, background: '#fff' }}>
            <Routes>
              <Route path="/" element={<ChatInterface />} />
              <Route path="/analysis" element={<DataAnalysis />} />
            </Routes>
          </Content>
        </Layout>
      </Layout>
    </Router>
  );
};

export default App; 