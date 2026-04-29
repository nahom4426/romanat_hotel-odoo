import psycopg2

try:
    # Connect with postgres user (password: passme)
    conn = psycopg2.connect(
        host='localhost',
        port=5432,
        user='postgres',
        password='passme',
        database='postgres'
    )
    
    cursor = conn.cursor()
    
    # Create odoo user
    try:
        cursor.execute("DROP USER IF EXISTS odoo;")
        print('✅ Dropped existing odoo user')
    except Exception as e:
        print(f'⚠️  Could not drop user: {e}')
    
    cursor.execute("CREATE USER odoo WITH PASSWORD 'odoo';")
    print('✅ Created user: odoo with password: odoo')
    
    # Grant superuser privileges (for development)
    cursor.execute("ALTER USER odoo CREATEDB SUPERUSER;")
    print('✅ Granted superuser privileges')
    
    conn.commit()
    cursor.close()
    conn.close()
    
    print('\n✅ Odoo user created successfully!')
    
except Exception as e:
    print(f'❌ Error: {e}')
    print('\nMake sure PostgreSQL is running and password is correct')
