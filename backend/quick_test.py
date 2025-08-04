import mysql.connector

print("⏳ Testing minimal MySQL connection...")

try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="wrongpass",  # Force an error
        connection_timeout=5
    )
    print("✅ Connected (unexpected)")
except Exception as e:
    print("❌ Got expected error:")
    print(e)
