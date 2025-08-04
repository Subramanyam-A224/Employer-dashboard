import React, { useEffect, useState } from 'react';
import { getEmployees, deleteEmployee } from '../api';
import './ViewEmployee.css'; // We'll add custom styles here

function ViewEmployee() {
  const [employees, setEmployees] = useState([]);

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

  return (
    <div className="view-container">
      <h2>👥 Employee Directory</h2>

      {employees.length === 0 ? (
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
            {employees.map(emp => (
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
