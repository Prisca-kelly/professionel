import MySQLdb
import sys

try:
    # Connect to MySQL (without specifying a database first)
    conn = MySQLdb.connect(
        host="localhost",
        user="root",
        passwd=""
    )
    cursor = conn.cursor()
    
    print("Dropping database...")
    cursor.execute("DROP DATABASE IF EXISTS portail_enseignement_pro;")
    
    print("Creating database...")
    cursor.execute("CREATE DATABASE portail_enseignement_pro CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
    
    print("Database recreated successfully!")
    conn.commit()
    cursor.close()
    conn.close()
    
except MySQLdb.Error as e:
    print(f"MySQL Error: {e}")
    sys.exit(1)
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
