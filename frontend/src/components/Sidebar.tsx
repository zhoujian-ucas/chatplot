import React from 'react';
import { Menu } from 'antd';
import { Link, useLocation } from 'react-router-dom';
import {
  MessageOutlined,
  BarChartOutlined,
} from '@ant-design/icons';
import './Sidebar.css';

const Sidebar: React.FC = () => {
  const location = useLocation();

  const menuItems = [
    {
      key: '/',
      icon: <MessageOutlined />,
      label: <Link to="/">Chat</Link>,
    },
    {
      key: '/analysis',
      icon: <BarChartOutlined />,
      label: <Link to="/analysis">Data Analysis</Link>,
    },
  ];

  return (
    <div className="sidebar">
      <div className="logo">
        <h2>ChatPlot</h2>
      </div>
      <Menu
        mode="inline"
        selectedKeys={[location.pathname]}
        items={menuItems}
        style={{ borderRight: 0 }}
      />
    </div>
  );
};

export default Sidebar; 