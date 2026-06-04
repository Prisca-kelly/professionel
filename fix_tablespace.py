import MySQLdb

conn = MySQLdb.connect(host='localhost', user='root', db='portail_enseignement_pro')
cursor = conn.cursor()

# Check for orphaned tablespaces
try:
    cursor.execute('SELECT TABLESPACE_NAME FROM INFORMATION_SCHEMA.INNODB_TABLESPACES WHERE TABLESPACE_NAME LIKE "%django%"')
    results = cursor.fetchall()
    print('Orphaned tablespaces:')
    for row in results:
        print(f'  - {row[0]}')
except Exception as e:
    print(f'Error checking tablespaces: {e}')

# Try to drop/recreate with FORCE option if available
try:
    cursor.execute('CREATE TABLE django_migrations (id INT PRIMARY KEY AUTO_INCREMENT, app VARCHAR(255), name VARCHAR(255), applied DATETIME DEFAULT CURRENT_TIMESTAMP)')
    print('django_migrations table created successfully')
    conn.commit()
except Exception as e:
    print(f'Error creating table: {e}')
    conn.rollback()

conn.close()
