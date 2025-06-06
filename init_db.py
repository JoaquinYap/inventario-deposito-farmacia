import sqlite3

conn = sqlite3.connect('inventario.db')
c = conn.cursor()

c.execute('''
CREATE TABLE IF NOT EXISTS insumos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo TEXT NOT NULL,
    subindice TEXT NOT NULL,
    descripcion TEXT NOT NULL,
    cantidad INTEGER NOT NULL,
    palet TEXT NOT NULL
)
''')

conn.commit()
conn.close()
