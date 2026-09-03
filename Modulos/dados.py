import json

usuarios_padrao = [
    {
        "login": "ARISTON",
        "senha": "123",
        "historico": [],
        "saldo": 10000
    },
    {
        "login": "DAVIZAO",
        "senha": "0123",
        "historico": [],
        "saldo": 10000
    },
    {
        "login": "ALEK",
        "senha": "1230",
        "historico": [],
        "saldo": 10000
    }
]

def carregar_usuarios():
    try:
        with open("usuarios.json", "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    except FileNotFoundError:
        return usuarios_padrao

def salvar_dados():
    with open("usuarios.json", "w", encoding="utf-8") as arquivo:
        json.dump(usuarios, arquivo, indent=4, ensure_ascii=False)

usuarios = carregar_usuarios()
usuario_logado = None