import MySQLdb
import sys

try:
    # Connect to MySQL
    conn = MySQLdb.connect(
        host="localhost",
        user="root",
        passwd="",
        db="portail_enseignement_pro"
    )
    cursor = conn.cursor()
    
    # Execute the DISCARD TABLESPACE command
    sql_cmd = "ALTER TABLESPACE `portail_enseignement_pro/django_migrations` DISCARD TABLESPACE"
    print(f"Executing: {sql_cmd}")
    cursor.execute(sql_cmd)
    
    print("Tablespace discarded successfully!")
    conn.commit()
    cursor.close()
    conn.close()
    
except MySQLdb.Error as e:
    print(f"MySQL Error: {e}")
    sys.exit(1)
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
