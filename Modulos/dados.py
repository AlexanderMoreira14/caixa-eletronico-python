import sqlite3

usuarios_padrao = [
    {"login": "ARISTON", "senha": "123", "saldo": 10000},
    {"login": "DAVIZAO", "senha": "0123", "saldo": 10000},
    {"login": "ALEK", "senha": "1230", "saldo": 10000}
]
def conectar():
    return sqlite3.connect('dados/caixa_eletronico.db')

def inicializar_banco():
    conexao = conectar()
    cursor = conexao.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS historico (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            login_usuario TEXT NOT NULL,
            registro TEXT NOT NULL
        )
    ''')
    
    cursor.execute("select count(*) from usuarios")
    quantidade = cursor.fetchone()[0]
    
    if quantidade == 0:
        for u in usuarios_padrao:
            cursor.execute(
                "INSERT INTO usuarios (login, senha, saldo) VALUES (?, ?, ?)",
                (u['login'], u['senha'], u['saldo']))
        
        print("Usuários padrão inseridos no banco de dados")
    conexao.commit()
    conexao.close()
    
def carregar_usuarios():
    conexao = conectar()
    cursor = conexao.cursor()
    
    cursor.execute("SELECT login, senha, saldo FROM usuarios")
    linhas = cursor.fetchall()
    conexao.close()
    
    lista_usuarios = []
    for linha in linhas:
        usuario = {
            "login": linha[0],
            "senha": linha[1],
            "saldo": linha[2],
            "historico": []
        }
        lista_usuarios.append(usuario)
        
    return lista_usuarios

def registrar_historico(login_usuario, registro):
    conexao = conectar()
    cursor = conexao.cursor()
    
    # Inserimos a transação na tabela, ligando-a ao login do utilizador
    cursor.execute('''
        INSERT INTO historico (login_usuario, registro)
        VALUES (?, ?)
    ''', (login_usuario, registro))
    
    conexao.commit()
    conexao.close()
    
def carregar_historico(login_usuario):
    conexao = conectar()
    cursor = conexao.cursor()
    
    # Busca apenas os registos ONDE o login for igual ao do utilizador logado
    cursor.execute("SELECT registro FROM historico WHERE login_usuario = ?", (login_usuario,))
    linhas = cursor.fetchall()
    conexao.close()
    
    # Transforma o resultado do banco numa lista normal do Python
    lista_historico = []
    for linha in linhas:
        lista_historico.append(linha[0])
        
    return lista_historico

def salvar_dados():
    conexao = conectar()
    cursor = conexao.cursor()
    
    for u in usuarios:
        cursor.execute('''
                      update usuarios
                      set saldo = ?
                      where login = ?
                      ''', (u['saldo'], u['login']))
    conexao.commit()
    conexao.close()
    

inicializar_banco()
usuarios = carregar_usuarios()
usuario_logado = None
