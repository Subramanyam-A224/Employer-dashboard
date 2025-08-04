import tornado.ioloop
import traceback
import tornado.web
import json
import datetime
from db import db_connection  # Assumes you're using PyMySQL in db.py

class EmployeesHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "Content-Type")
        self.set_header("Access-Control-Allow-Methods", "GET, POST, DELETE, OPTIONS")
        self.set_header("Content-Type", "application/json")

    def options(self):
        self.set_status(204)
        self.finish()

    def get(self):
        try:
            conn = db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM employees")
            rows = cursor.fetchall()

            # Convert to list of dicts and serialize datetime
            employees = []
            columns = [desc[0] for desc in cursor.description]
            for row in rows:
                emp_dict = {}
                for i, col in enumerate(columns):
                    value = row[i]
                    if isinstance(value, (datetime.datetime, datetime.date)):
                        value = value.isoformat()
                    emp_dict[col] = value
                employees.append(emp_dict)


            self.write(json.dumps(employees))
        except Exception as e:
            print("❌ Error in GET:", e)
            self.set_status(500)
            self.write(json.dumps({"error": str(e)}))
        finally:
            if 'cursor' in locals(): cursor.close()
            if 'conn' in locals(): conn.close()

    def post(self):
        try:
            data = json.loads(self.request.body)
            print("✅ Received data:", data)

            conn = db_connection()
            cursor = conn.cursor()

            sql = "INSERT INTO employees (name, email, designation) VALUES (%s, %s, %s)"
            values = (data['name'], data['email'], data['designation'])

            cursor.execute(sql, values)
            conn.commit()

            print("✅ Employee added to database")
            self.set_status(200)
            self.write(json.dumps({"status": "success"}))

        except Exception as e:
            print("❌ Exception occurred:")
            traceback.print_exc()
            self.set_status(500)
            self.write(json.dumps({"error": str(e)}))

        finally:
            if 'cursor' in locals(): cursor.close()
            if 'conn' in locals(): conn.close()


class DeleteEmployeeHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "Content-Type")
        self.set_header("Access-Control-Allow-Methods", "DELETE, OPTIONS")
        self.set_header("Content-Type", "application/json")

    def options(self, emp_id):
        self.set_status(204)
        self.finish()

    def delete(self, emp_id):
        try:
            conn = db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM employees WHERE id = %s", (emp_id,))
            conn.commit()
            self.write(json.dumps({"status": "deleted"}))
        except Exception as e:
            print("❌ Error deleting employee:", str(e))
            self.set_status(500)
            self.write(json.dumps({"error": str(e)}))
        finally:
            if 'cursor' in locals(): cursor.close()
            if 'conn' in locals(): conn.close()


# ✅ NEW: DashboardStatsHandler for /dashboard-stats
class DashboardStatsHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Content-Type", "application/json")

    def get(self):
        try:
            conn = db_connection()
            cursor = conn.cursor()

            # 1. Total number of employees
            cursor.execute("SELECT COUNT(*) FROM employees")
            total_employees = cursor.fetchone()[0]

            # 2. Total unique designations
            cursor.execute("SELECT COUNT(DISTINCT designation) FROM employees")
            total_designations = cursor.fetchone()[0]

            # 3. Most recently added employee
            cursor.execute("SELECT id, name, email, designation, created_at FROM employees ORDER BY created_at DESC LIMIT 1")
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
                "total_employees": total_employees,
                "total_designations": total_designations,
                "latest_employee": latest_employee
            }))

        except Exception as e:
            print("❌ Error fetching dashboard stats:", str(e))
            self.set_status(500)
            self.write(json.dumps({"error": str(e)}))
        finally:
            if 'cursor' in locals(): cursor.close()
            if 'conn' in locals(): conn.close()


def make_app():
    return tornado.web.Application([
        (r"/employees", EmployeesHandler),
        (r"/employees/([0-9]+)", DeleteEmployeeHandler),
        (r"/dashboard-stats", DashboardStatsHandler),  # ✅ New route
    ])


if __name__ == "__main__":
    try:
        app = make_app()
        app.listen(8888)
        print("✅ Backend running at http://localhost:8888")
        tornado.ioloop.IOLoop.current().start()
    except Exception as e:
        print("❌ Server crashed on startup:")
        traceback.print_exc()
