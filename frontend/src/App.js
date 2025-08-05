import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import AddEmployee from './pages/AddEmployee';
import ViewEmployee from './pages/ViewEmployee';
import './App.css'; // NEW - import custom styling

function App() {
  return (
    <Router>
      <div className="app-container">
        <nav className="navbar">
          <div className="nav-logo">👨‍💼 Employer Dashboard</div>
          <div className="nav-links">
            <Link to="/" className="nav-link">🏠 Dashboard</Link>
            <Link to="/add" className="nav-link">➕ Add Employee</Link>
            <Link to="/view" className="nav-link">📋 View Employees</Link>
          </div>
        </nav>

        <div className="content">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/add" element={<AddEmployee />} />
            <Route path="/view" element={<ViewEmployee />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;
