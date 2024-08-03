from flask import render_template, request, redirect, url_for
from app import app
import mysql.connector
from app.config import Config

def get_db_connection():
    conn = mysql.connector.connect(**Config.DATABASE_CONFIG)
    return conn

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        nome = request.form['nome']
        senha = request.form['senha']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM professor WHERE nome=%s AND senha=%s", (nome, senha))
        professor = cursor.fetchone()
        conn.close()
        
        if professor:
            return redirect(url_for('notas'))
        else:
            return "Nome ou senha incorretos!"
    
    return render_template('index.html')

@app.route('/notas', methods=['GET', 'POST'])
def notas():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if request.method == 'POST' and 'nome_aluno' in request.form:
        nome_aluno = request.form['nome_aluno']
        nota = float(request.form['nota'])
        
        cursor.execute("INSERT INTO aluno (nome) VALUES (%s)", (nome_aluno,))
        conn.commit()
        
        cursor.execute("SELECT rm FROM aluno WHERE nome=%s", (nome_aluno,))
        aluno_rm = cursor.fetchone()[0]
        
        cursor.execute("INSERT INTO nota (aluno_rm, nota) VALUES (%s, %s)", (aluno_rm, nota))
        conn.commit()
    
    cursor.execute("""
        SELECT aluno.nome, nota.nota 
        FROM aluno 
        INNER JOIN nota ON aluno.rm = nota.aluno_rm
    """)
    notas = cursor.fetchall()
    
    conn.close()
    
    return render_template('notas.html', notas=notas)
