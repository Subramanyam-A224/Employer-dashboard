import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link, useNavigate } from 'react-router-dom';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import AddEmployee from './pages/AddEmployee';
import ViewEmployee from './pages/ViewEmployee';
import ProtectedRoute from './ProtectedRoute';
import './App.css';

function Navbar() {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem('isLoggedIn');
    navigate('/');
  };

  return (
    <nav className="navbar">
      <div className="nav-logo">👨‍💼 Employer Dashboard</div>
      <div className="nav-links">
        <Link to="/dashboard" className="nav-link">🏠 Dashboard</Link>
        <Link to="/add" className="nav-link">➕ Add Employee</Link>
        <Link to="/view" className="nav-link">📋 View Employees</Link>
        <button onClick={handleLogout} className="nav-link logout-btn">🚪 Logout</button>
      </div>
    </nav>
  );
}

function AppWrapper() {
  return (
    <Router>
      <div className="app-container">
        <Navbar />
        <div className="content">
          <Routes>
            <Route path="/" element={<Login />} />
            <Route
              path="/dashboard"
              element={
                <ProtectedRoute>
                  <Dashboard />
                </ProtectedRoute>
              }
            />
            <Route
              path="/add"
              element={
                <ProtectedRoute>
                  <AddEmployee />
                </ProtectedRoute>
              }
            />
            <Route
              path="/view"
              element={
                <ProtectedRoute>
                  <ViewEmployee />
                </ProtectedRoute>
              }
            />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default AppWrapper;
