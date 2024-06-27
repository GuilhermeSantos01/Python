import mysql.connector
from getpass import getpass

# Configurações de conexão
config = {'user': 'root','password': '0321','host': 'localhost','database': 'escola',}

# Conectar ao banco de dados
connector = mysql.connector.connect(**config)
cursor = connector.cursor()

# Função para verificar o login do professor
def verificar_professor():
    nome = input("Nome do professor: ")
    senha = getpass("Senha do professor: ")
    
    query = "SELECT * FROM professor WHERE nome=%s AND senha=%s"
    cursor.execute(query, (nome, senha))
    resultado = cursor.fetchone()
    
    if resultado:
        return True
    else:
        print("Nome ou senha incorretos.")
        return False

# Função para inserir notas
def inserir_notas():
    notas = []
    quantidade_de_alunos = int(input("Quantidades de notas: "))

    for x in range(quantidade_de_alunos):
        rm = input("RM: ")
        nota = float(input("Nota: "))
        notas.append((rm, nota))

    query = "INSERT INTO nota (aluno_rm, nota) VALUES (%s, %s)"
    cursor.executemany(query, notas)
    connector.commit()
    print("Notas inseridas com sucesso.")

# Função para exibir as notas dos alunos
def exibir_notas():
    query = "SELECT aluno_rm, nota FROM nota"
    cursor.execute(query)
    resultados = cursor.fetchall()

    print("\nRM do aluno\tNota")
    for aluno_rm, nota in resultados:
        print(f"{aluno_rm}\t\t{nota}")

# Função principal
def main():
    if verificar_professor():
        inserir_notas()
        ver_notas = input("Deseja ver as notas de todos os alunos? Sim ou Não: ").lower()
        if ver_notas == "sim":
            exibir_notas()

if __name__ == '__main__':
    main()

# Fechar a conexão
cursor.close()
connector.close()



