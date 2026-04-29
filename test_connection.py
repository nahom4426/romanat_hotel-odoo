import psycopg2

try:
    conn = psycopg2.connect(
        host='localhost',
        port=5432,
        user='odoo',
        password='odoo',
        database='postgres'
    )
    print('✅ Odoo user connection successful!')
    conn.close()
except Exception as e:
    print(f'❌ Odoo user connection failed: {e}')