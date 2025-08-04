import tornado.ioloop
import traceback
import tornado.web
import json
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

            # Convert to list of dicts
            employees = []
            columns = [desc[0] for desc in cursor.description]
            for row in rows:
                employees.append(dict(zip(columns, row)))

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

            print("📥 Executing SQL Query:", sql)
            print("📦 With values:", values)

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


def make_app():
    return tornado.web.Application([
        (r"/employees", EmployeesHandler),
        (r"/employees/([0-9]+)", DeleteEmployeeHandler),
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
