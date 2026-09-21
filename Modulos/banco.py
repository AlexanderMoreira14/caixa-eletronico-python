import sqlite3

conexao = sqlite3.connect('Dados/caixa_eletronico.db')
cursor = conexao.cursor()

cursor.execute('''
create table if not exists usuarios(
    id integer primary key autoincrement,
    login text unique not null,
    senha text not null,
    saldo real default 0.0
)''')

conexao.commit()
conexao.close()
print("tabela 'usuarios' criado com sucesso")