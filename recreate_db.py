import psycopg2

try:
    # Connect to PostgreSQL with odoo user
    conn = psycopg2.connect(
        host='localhost',
        port=5432,
        user='odoo',
        password='odoo',
        database='postgres'
    )
    conn.autocommit = True
    cursor = conn.cursor()
    
    # Drop database if exists
    cursor.execute("DROP DATABASE IF EXISTS odoo18;")
    print('✅ Dropped database odoo18')
    
    # Create fresh database
    cursor.execute("CREATE DATABASE odoo18;")
    print('✅ Created fresh database odoo18')
    
    cursor.close()
    conn.close()
    print('✅ Database ready for Odoo initialization')
    
except Exception as e:
    print(f'❌ Error: {e}')
    print('\nMake sure:')
    print('1. PostgreSQL service is running')
    print('2. User odoo exists and has privileges')