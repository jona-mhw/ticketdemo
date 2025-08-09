import sqlite3
conn = sqlite3.connect('demo_tickethome.db')
cursor = conn.cursor()
cursor.execute('SELECT name FROM sqlite_master WHERE type=\'table\';')
tables = cursor.fetchall()
for table_name in tables:
    table_name = table_name[0]
    print(f'\n--- Table: {table_name} ---')
    cursor.execute(f'PRAGMA table_info({table_name});')
    columns = cursor.fetchall()
    print('Schema:', columns)
    cursor.execute(f'SELECT * FROM {table_name} LIMIT 5;')
    rows = cursor.fetchall()
    print('Data:')
    for row in rows:
        print(row)
conn.close()