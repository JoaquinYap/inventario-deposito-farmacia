import os
from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

DB = 'inventario.db'

def init_db():
    with sqlite3.connect(DB) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS insumos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                codigo TEXT NOT NULL,
                subindice TEXT NOT NULL,
                descripcion TEXT NOT NULL,
                cantidad INTEGER NOT NULL
            )
        """)

@app.route('/')
def index():
    with sqlite3.connect(DB) as conn:
        insumos = conn.execute("SELECT * FROM insumos").fetchall()
    return render_template('index.html', insumos=insumos)

@app.route('/agregar', methods=['GET', 'POST'])
def agregar():
    if request.method == 'POST':
        codigo = request.form['codigo']
        subindice = request.form['subindice']
        descripcion = request.form['descripcion']
        cantidad = int(request.form['cantidad'])

        with sqlite3.connect(DB) as conn:
            conn.execute('INSERT INTO insumos (codigo, subindice, descripcion, cantidad) VALUES (?, ?, ?, ?)',
                         (codigo, subindice, descripcion, cantidad))
        return redirect('/')
    return render_template('agregar.html')
@app.route('/eliminar/<int:id>')
def eliminar(id):
    with sqlite3.connect(DB) as conn:
        conn.execute('DELETE FROM insumos WHERE id = ?', (id,))
    return redirect('/')

@app.route('/modificar/<int:id>/<accion>')
def modificar(id, accion):
    with sqlite3.connect(DB) as conn:
        insumo = conn.execute('SELECT cantidad FROM insumos WHERE id = ?', (id,)).fetchone()
        if insumo:
            cantidad = insumo[0] + 1 if accion == 'entrada' else max(0, insumo[0] - 1)
            conn.execute('UPDATE insumos SET cantidad = ? WHERE id = ?', (cantidad, id))
    return redirect('/')

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    conn = sqlite3.connect('insumos.db')
    cursor = conn.cursor()

    if request.method == 'POST':
        codigo = request.form['codigo']
        subindice = request.form['subindice']
        descripcion = request.form['descripcion']
        cantidad = request.form['cantidad']

        cursor.execute('''
            UPDATE insumos
            SET codigo = ?, subindice = ?, descripcion = ?, cantidad = ?
            WHERE id = ?
        ''', (codigo, subindice, descripcion, cantidad, id))
        conn.commit()
        conn.close()
        return redirect('/')

    cursor.execute('SELECT * FROM insumos WHERE id = ?', (id,))
    insumo = cursor.fetchone()
    conn.close()

    return render_template('editar.html', insumo=insumo)


if __name__ == '__main__':
    init_db()
    port = int(os.environ.get("PORT", 5000)) 
    app.run(host='0.0.0.0', port=port)
    
