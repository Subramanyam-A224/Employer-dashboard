import tornado.ioloop
import tornado.web
import traceback
import json
import datetime
from db import db_connection  # Custom DB connection using PyMySQL


# ✅ BaseHandler for shared behavior across handlers
class BaseHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "Content-Type")
        self.set_header("Access-Control-Allow-Methods", "GET, POST, DELETE, OPTIONS")
        self.set_header("Content-Type", "application/json")

    def options(self, *args, **kwargs):
        self.set_status(204)
        self.finish()


# ✅ GET /employees, POST /employees
class EmployeesHandler(BaseHandler):
    def get(self):
        try:
            conn = db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM employees")
            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            employees = []

            for row in rows:
                emp_dict = {}
                for i, col in enumerate(columns):
                    value = row[i]
                    if isinstance(value, (datetime.datetime, datetime.date)):
                        value = value.isoformat()
                    emp_dict[col] = value
                employees.append(emp_dict)

            self.write(json.dumps({"status": "success", "data": employees}))
        except Exception as e:
            traceback.print_exc()
            self.set_status(500)
            self.write(json.dumps({"status": "fail", "error": str(e)}))
        finally:
            if 'cursor' in locals(): cursor.close()
            if 'conn' in locals(): conn.close()

    def post(self):
        try:
            data = json.loads(self.request.body)
            conn = db_connection()
            cursor = conn.cursor()

            sql = "INSERT INTO employees (name, email, designation) VALUES (%s, %s, %s)"
            values = (data['name'], data['email'], data['designation'])
            cursor.execute(sql, values)
            conn.commit()

            self.write(json.dumps({"status": "success", "message": "Employee added successfully"}))
        except Exception as e:
            traceback.print_exc()
            self.set_status(500)
            self.write(json.dumps({"status": "fail", "error": str(e)}))
        finally:
            if 'cursor' in locals(): cursor.close()
            if 'conn' in locals(): conn.close()


# ✅ DELETE /employees/<id>
class DeleteEmployeeHandler(BaseHandler):
    def delete(self, emp_id):
        try:
            conn = db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM employees WHERE id = %s", (emp_id,))
            conn.commit()
            self.write(json.dumps({"status": "success", "message": "Employee deleted"}))
        except Exception as e:
            traceback.print_exc()
            self.set_status(500)
            self.write(json.dumps({"status": "fail", "error": str(e)}))
        finally:
            if 'cursor' in locals(): cursor.close()
            if 'conn' in locals(): conn.close()


# ✅ GET /dashboard-stats
class DashboardStatsHandler(BaseHandler):
    def get(self):
        try:
            conn = db_connection()
            cursor = conn.cursor()

            cursor.execute("SELECT COUNT(*) FROM employees")
            total_employees = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(DISTINCT designation) FROM employees")
            total_designations = cursor.fetchone()[0]

            cursor.execute("""
                SELECT id, name, email, designation, created_at 
                FROM employees ORDER BY created_at DESC LIMIT 1
            """)
            row = cursor.fetchone()
            latest_employee = None
            if row:
                latest_employee = {
                    "id": row[0],
                    "name": row[1],
                    "email": row[2],
                    "designation": row[3],
                    "created_at": row[4].isoformat() if row[4] else None
                }

            self.write(json.dumps({
                "status": "success",
                "data": {
                    "total_employees": total_employees,
                    "total_designations": total_designations,
                    "latest_employee": latest_employee
                }
            }))
        except Exception as e:
            traceback.print_exc()
            self.set_status(500)
            self.write(json.dumps({"status": "fail", "error": str(e)}))
        finally:
            if 'cursor' in locals(): cursor.close()
            if 'conn' in locals(): conn.close()


# ✅ POST /admin/login
class AdminLoginHandler(BaseHandler):
    def post(self):
        try:
            data = json.loads(self.request.body)
            email = data.get("email")
            password = data.get("password")

            conn = db_connection()
            cursor = conn.cursor()
            sql = "SELECT * FROM admins WHERE email = %s AND password = %s"
            cursor.execute(sql, (email, password))
            admin = cursor.fetchone()

            if admin:
                self.write(json.dumps({"status": "success", "message": "Login successful"}))
            else:
                self.set_status(401)
                self.write(json.dumps({"status": "fail", "message": "Invalid credentials"}))
        except Exception as e:
            traceback.print_exc()
            self.set_status(500)
            self.write(json.dumps({"status": "fail", "error": str(e)}))
        finally:
            if 'cursor' in locals(): cursor.close()
            if 'conn' in locals(): conn.close()


# ✅ Application setup
def make_app():
    return tornado.web.Application([
        (r"/employees", EmployeesHandler),
        (r"/employees/([0-9]+)", DeleteEmployeeHandler),
        (r"/dashboard-stats", DashboardStatsHandler),
        (r"/admin/login", AdminLoginHandler),
    ])


# ✅ Entry point
if __name__ == "__main__":
    try:
        app = make_app()
        app.listen(8888)
        print("✅ Backend running at http://localhost:8888")
        tornado.ioloop.IOLoop.current().start()
    except Exception as e:
        print("❌ Server crashed on startup:")
        traceback.print_exc()
