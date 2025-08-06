// src/pages/Dashboard.js

import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './Dashboard.css'; // We’ll style it with a nice gradient and cards

function Dashboard() {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchStats();
  }, []);

  const fetchStats = async () => {
    try {
      const response = await axios.get('http://localhost:8888/dashboard-stats');
      setStats(response.data);
    } catch (err) {
      console.error('❌ Failed to fetch dashboard stats:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="dashboard-container">
      <h2 className="dashboard-title">📊 Dashboard Overview</h2>

      {loading ? (
        <p className="loading">Loading stats...</p>
      ) : stats ?.data ? (
        <div className="cards">
          <div className="card">
            <h3>Total Employees</h3>
            <p>{stats.data.total_employees}</p>
          </div>

          <div className="card">
            <h3>Unique Designations</h3>
            <p>{stats.data.total_designations}</p>
          </div>

          <div className="card latest-card">
            <h3>Recently Added</h3>
            {stats.data.latest_employee ? (
              <div className="latest-emp">
                <p><strong>Name:</strong> {stats.data.latest_employee.name}</p>
                <p><strong>Email:</strong> {stats.data.latest_employee.email}</p>
                <p><strong>Role:</strong> {stats.data.latest_employee.designation}</p>
                <p><strong>Added:</strong> {new Date(stats.data.latest_employee.created_at).toLocaleString()}</p>
              </div>
            ) : (
              <p>No employees yet.</p>
            )}
          </div>
        </div>
      ) : (
        <p className="error">Something went wrong 😔</p>
      )}
    </div>
  );
}

export default Dashboard;
