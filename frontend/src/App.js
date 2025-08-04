import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import AddEmployee from './pages/AddEmployee';
import ViewEmployee from './pages/ViewEmployee';

function App() {
  return (
    <Router>
      <div className="App">
        <nav style={{ margin: '20px' }}>
          <Link to="/" style={{ marginRight: '15px' }}>🏠 Dashboard</Link>
          <Link to="/add" style={{ marginRight: '15px' }}>➕ Add Employee</Link>
          <Link to="/view">📋 View Employees</Link>
        </nav>

        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/add" element={<AddEmployee />} />
          <Route path="/view" element={<ViewEmployee />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
