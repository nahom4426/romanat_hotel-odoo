import psycopg2

print('Testing PostgreSQL connection...')
print('Service: postgresql-x64-17 (already running)')
print('Host: localhost, Port: 5432, User: postgres')
print()

# Common passwords to try
passwords = [
    'postgres',    # Most common default
    'admin',
    'password',
    'odoo',
    'passme',            # Empty password
    'Postgres',
    'PostgreSQL',
    '123456',
    'postgres17',
    'postgres123'
]

for pwd in passwords:
    try:
        conn = psycopg2.connect(
            host='localhost',
            port=5432,
            user='postgres',
            password=pwd,
            database='postgres'
        )
        print(f'✅ SUCCESS! Connected with password: "{pwd}"')
        
        # Test if we can create database
        cursor = conn.cursor()
        cursor.execute('SELECT version();')
        version = cursor.fetchone()[0]
        print(f'   PostgreSQL Version: {version}')
        
        cursor.close()
        conn.close()
        break
    except psycopg2.OperationalError as e:
        if 'password authentication failed' in str(e):
            print(f'❌ Failed with password: "{pwd}"')
        else:
            print(f'❌ Error with "{pwd}": {e}')
    except Exception as e:
        print(f'❌ Unexpected error: {e}')
else:
    print('\n⚠️  Could not connect with any common password.')
    print('\nNext steps:')
    print('1. Open pgAdmin 4 (you have it installed)')
    print('2. Check what password you used during installation')
    print('3. Or reset the password in pgAdmin')