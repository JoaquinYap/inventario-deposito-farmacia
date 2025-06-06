from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('inventario.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    insumos = conn.execute('SELECT * FROM insumos').fetchall()
    conn.close()
    return render_template('index.html', insumos=insumos)

@app.route('/agregar', methods=['GET', 'POST'])
def agregar():
    if request.method == 'POST':
        datos = (
            request.form['codigo'],
            request.form['subindice'],
            request.form['descripcion'],
            request.form['cantidad'],
            request.form['palet']
        )
        conn = get_db_connection()
        conn.execute('INSERT INTO insumos (codigo, subindice, descripcion, cantidad, palet) VALUES (?, ?, ?, ?, ?)', datos)
        conn.commit()
        conn.close()
        return redirect('/')
    return render_template('agregar.html')

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    conn = get_db_connection()
    if request.method == 'POST':
        datos = (
            request.form['codigo'],
            request.form['subindice'],
            request.form['descripcion'],
            request.form['cantidad'],
            request.form['palet'],
            id
        )
        conn.execute('''
            UPDATE insumos
            SET codigo = ?, subindice = ?, descripcion = ?, cantidad = ?, palet = ?
            WHERE id = ?''', datos)
        conn.commit()
        conn.close()
        return redirect('/')
    insumo = conn.execute('SELECT * FROM insumos WHERE id = ?', (id,)).fetchone()
    conn.close()
    return render_template('editar.html', insumo=insumo)

@app.route('/eliminar/<int:id>')
def eliminar(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM insumos WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/palets/<string:nombre_palet>')
def ver_palet_individual(nombre_palet):
    conn = get_db_connection()
    insumos = conn.execute('SELECT * FROM insumos WHERE palet = ?', (nombre_palet,)).fetchall()
    conn.close()
    return render_template('palet_individual.html', nombre_palet=nombre_palet, insumos=insumos)

@app.route('/palets')
def ver_palets():
    conn = get_db_connection()
    datos = conn.execute('SELECT * FROM insumos').fetchall()
    conn.close()
    palets = {}
    for insumo in datos:
        palets.setdefault(insumo['palet'], []).append(insumo)
    return render_template('palets.html', palets=palets)

import os

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)

