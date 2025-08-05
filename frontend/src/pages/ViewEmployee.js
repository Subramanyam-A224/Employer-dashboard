import React, { useEffect, useState } from 'react';
import { getEmployees, deleteEmployee } from '../api';
import './ViewEmployee.css';

function ViewEmployee() {
  const [employees, setEmployees] = useState([]);
  const [searchQuery, setSearchQuery] = useState('');

  useEffect(() => {
    loadEmployees();
  }, []);

  const loadEmployees = async () => {
    const data = await getEmployees();
    setEmployees(data);
  };

  const handleDelete = async (id) => {
    const confirmDelete = window.confirm("❗ Are you sure you want to delete this employee?");
    if (confirmDelete) {
      await deleteEmployee(id);
      loadEmployees();
    }
  };

  const filteredEmployees = employees.filter((emp) =>
    emp.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
    emp.email.toLowerCase().includes(searchQuery.toLowerCase()) ||
    emp.designation.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <div className="view-container">
      <h2>👥 Employee Directory</h2>

      {/* 🔍 Search Input */}
      <input
        type="text"
        placeholder="🔍 Search by name, email, or designation..."
        className="search-box"
        value={searchQuery}
        onChange={(e) => setSearchQuery(e.target.value)}
      />

      {filteredEmployees.length === 0 ? (
        <p className="no-emp-msg">No employees found 👻</p>
      ) : (
        <table className="emp-table">
          <thead>
            <tr>
              <th>🆔 ID</th>
              <th>🧑 Name</th>
              <th>📧 Email</th>
              <th>💼 Designation</th>
              <th>🛠️ Actions</th>
            </tr>
          </thead>
          <tbody>
            {filteredEmployees.map(emp => (
              <tr key={emp.id}>
                <td>{emp.id}</td>
                <td>{emp.name}</td>
                <td>{emp.email}</td>
                <td>{emp.designation}</td>
                <td>
                  <button className="delete-btn" onClick={() => handleDelete(emp.id)}>
                    🗑️ Delete
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}

export default ViewEmployee;
