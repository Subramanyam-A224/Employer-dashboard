from db import db_connection

print("🧪 Connecting to MySQL with PyMySQL...")

try:
    conn = db_connection()
    print("✅ Connected successfully!")

    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM employees")
        rows = cursor.fetchall()
        print(f"👨‍💼 Rows in 'employees' table: {len(rows)}")
        for row in rows:
            print(row)

except Exception as e:
    print("❌ Error connecting to DB:")
    import traceback
    traceback.print_exc()

finally:
    if 'conn' in locals():
        conn.close()
        print("🔌 Connection closed.")
