const API_BASE = "http://localhost:8888"; // ✅ corrected port

// GET: Fetch all employees
export async function getEmployees() {
  try {
    const response = await fetch(`${API_BASE}/employees`);
    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Error fetching employees:", error);
    return [];
  }
}

// POST: Add new employee
export async function addEmployee(employee) {
  try {
    const response = await fetch(`${API_BASE}/employees`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(employee)
    });
    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Error adding employee:", error);
    return { status: "error" };
  }
}

export async function deleteEmployee(id) {
    try {
      const response = await fetch(`${API_BASE}/employees/${id}`, {
        method: "DELETE"
      });
      const data = await response.json();
      return data;
    } catch (error) {
      console.error("Error deleting employee:", error);
      return { status: "error" };
    }
  }
  