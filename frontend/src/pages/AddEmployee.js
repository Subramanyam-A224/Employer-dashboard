import React, { useState } from 'react';
import axios from 'axios';
import './AddEmployee.css'; // Import the CSS file

function AddEmployee() {
  const [employee, setEmployee] = useState({
    name: '',
    email: '',
    designation: ''
  });

  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setEmployee((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const response = await axios.post('http://localhost:8888/employees', employee, {
        headers: { 'Content-Type': 'application/json' }
      });

      if (response.status === 200 && response.data.status === 'success') {
        alert('✅ Employee added successfully!');
        setEmployee({ name: '', email: '', designation: '' });
      } else {
        alert('⚠️ Unexpected server response');
        console.error('⚠️ Full Response:', response.data);
      }
    } catch (error) {
      alert('❌ Error adding employee');
      console.error('❌ Axios Error:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="add-employee-container">
      <div className="form-card">
        <h2 className="form-title">➕ Add New Employee</h2>
        <form onSubmit={handleSubmit} className="employee-form">
          <input
            type="text"
            name="name"
            placeholder="Full Name"
            value={employee.name}
            onChange={handleChange}
            required
            className="form-input"
          />
          <input
            type="email"
            name="email"
            placeholder="Email"
            value={employee.email}
            onChange={handleChange}
            required
            className="form-input"
          />
          <input
            type="text"
            name="designation"
            placeholder="Designation"
            value={employee.designation}
            onChange={handleChange}
            required
            className="form-input"
          />
          <button type="submit" disabled={loading} className={`form-button ${loading ? 'disabled' : ''}`}>
            {loading ? 'Adding...' : 'Add Employee'}
          </button>
        </form>
      </div>
    </div>
  );
}

export default AddEmployee;
