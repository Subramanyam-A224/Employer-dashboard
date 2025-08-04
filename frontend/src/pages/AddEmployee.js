import React, { useState } from 'react';
import axios from 'axios';

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
        headers: {
          'Content-Type': 'application/json'
        }
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
    <div>
      <h2>➕ Add New Employee</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          name="name"
          placeholder="Full Name"
          value={employee.name}
          onChange={handleChange}
          required
        /><br /><br />
        <input
          type="email"
          name="email"
          placeholder="Email"
          value={employee.email}
          onChange={handleChange}
          required
        /><br /><br />
        <input
          type="text"
          name="designation"
          placeholder="Designation"
          value={employee.designation}
          onChange={handleChange}
          required
        /><br /><br />
        <button type="submit" disabled={loading}>
          {loading ? 'Adding...' : 'Add Employee'}
        </button>
      </form>
    </div>
  );
}

export default AddEmployee;
