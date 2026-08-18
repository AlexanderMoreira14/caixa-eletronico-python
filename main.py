from datetime import datetime
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
    
def realizar_login():
    global usuario_logado
    tentativas = 0
    while tentativas < 3:
        tentativas += 1
        login_input = input("Digite o seu login: ")
        senha_input = input("Digite a sua senha: ")
        
        for usuario in usuarios:
            if login_input.upper() == usuario["login"] and senha_input == usuario["senha"]:
                usuario_logado = usuario
                print(f"\nBem-vindo, {usuario['login']}!")
                return True
        else:
            print(f"Login ou senha incorretos. Tentativas restantes: {3 - tentativas}")                       
    print("Conta bloqueada.")
    return False

def realizar_menu():
    print("\n---- MENU BANCO ----")
    print("1 - Saque")
    print("2 - Depositar")
    print("3 - Extrato")
    print("4 - PIX")
    print("5 - Trocar de Usuário")
    print("6 - Cadastrar novo usuário")
    print("7 - Saldo")
    print("8 - Excluir usuário")
    print("9 - Sair do programa")
    return input("Escolha uma opção: ")
    
def realizar_saque():
    hora_atual = datetime.now()
    try:
        saque = float(input("Digite o valor do saque: "))
    except ValueError:
        print("Valor inválido. Por favor, digite um número.")
        return realizar_saque()
    if saque > 0 and saque <= usuario_logado['saldo']:
        usuario_logado["saldo"] -= saque
        usuario_logado["historico"].append(f"{hora_atual.strftime('%H:%M em %d/%m/%Y')}\nSaque: {saque:.2f}")
        salvar_dados()
        print(f"O saque no valor de R$ {saque:.2f} foi realizado")
        print(f"Seu saldo atual é de R$ {usuario_logado['saldo']:.2f}")
        
    else:
        print("Saldo insuficiente ou valor inválido.")
        return

def realizar_deposito():
    hora_atual = datetime.now()
    try:
        deposito = float(input("Digite o valor do depósito: "))
    except ValueError:
        print("Valor inválido. Por favor, digite um número.")
        return realizar_deposito()
    if deposito > 0:
        usuario_logado["saldo"] += deposito
        usuario_logado["historico"].append(f"{hora_atual.strftime('%H:%M em %d/%m/%Y')}\nDepósito: +R$ {deposito:.2f}")
        salvar_dados()
        print(f"O depósito no valor de R$ {deposito:.2f} foi feito com sucesso")
        print(f"Seu saldo atual é de R$ {usuario_logado['saldo']:.2f}")
        
    else:
        print("Valor inválido.")

def realizar_extrato():
    print(f"\n------ Extrato de {usuario_logado ['login']} ------")
    if not usuario_logado["historico"]:
        print("Nenhuma operação realizada.")
    else: 
        for operacao in usuario_logado["historico"]:
            print(operacao)    
    print(f"Saldo: -R$ {usuario_logado['saldo']:.2f}")
    print("=======================")

def realizar_pix():
    hora_atual = datetime.now()
    destino = input("Digite o login do usuário para transferir: ")
    try:
        valor = float(input("Digite o valor da transferência: "))
    except ValueError:
        print("Valor inválido. Por favor, digite um número.")
        return realizar_pix()
    
    for usuario in usuarios:
        if usuario["login"] == destino.upper():
            
            if usuario == usuario_logado:
                print ("Você não pode fazer PIX para a própria conta.")
                return
            
            if valor > 0 and valor <= usuario_logado["saldo"]:
                usuario_logado["saldo"] -= valor
                usuario["saldo"] += valor
                usuario_logado["historico"].append(f"{hora_atual.strftime('%H:%M em %d/%m/%Y')}\nTransferência realizada para {destino.upper()}: -R$ {valor:.2f}")
                usuario["historico"].append(f"{hora_atual.strftime('%H:%M em %d/%m/%Y')}\nTransferência recebida de {usuario_logado['login']}: +R$ {valor:.2f}")
                salvar_dados()
                print(f"Transferência de R$ {valor:.2f} para {destino.upper()} realizada com sucesso.")
                return
            
            else:
                print("Saldo insuficiente ou valor inválido.")
                return
            
    print("Este usuário não existe")
        
def consultar_saldo():
    print(f"Seu saldo atual é de R$ {usuario_logado['saldo']:.2f}")
    
def trocar_usuario():
    global usuario_logado
    usuario_logado = None
    if realizar_login():
        return True
    else:
        return False

def realizar_sair():
    print("Você saiu do caixa. Até logo!")

def cadastrar_usuario():
    
    cadastro_novo = input("Digite novo usuário:").upper().strip()
    for usuario in usuarios:
     if cadastro_novo == usuario["login"]:
        print("Usuário já existe.")
        return
    
    cadastro_senha = input("Digite a senha do novo usuário:")

    usuarios_novos = {
            "login": cadastro_novo,
            "senha": cadastro_senha,
            "historico": [],
            "saldo": 0
        }

    usuarios.append(usuarios_novos)
    salvar_dados()
    print(f"Usuário {cadastro_novo} cadastrado com sucesso!")
    return realizar_login()

def excluir_usuario():
    global usuario_logado
    confirmacao = input(f"Tem certeza que deseja excluir o usuário {usuario_logado['login']}?\n Digite apenas SIM ou NÃO: ").upper()
    if confirmacao == "SIM":
        tentativas = 0
        while tentativas < 3:
            tentativas += 1
            senha_confirmacao = input("Digite a senha do usuário para confirmar a exclusão: ")
            if senha_confirmacao == usuario_logado['senha']:
                usuarios.remove(usuario_logado)
                salvar_dados()
                print(f"Usuário {usuario_logado['login']} excluído com sucesso.")
                usuario_logado = None
                return realizar_login()
            else:
                print(f"Senha incorreta. Tentativas restantes: {3 - tentativas}")
                if tentativas == 3:
                    print("Número máximo de tentativas atingido. Exclusão cancelada.")
                    return
    else:
        print("Exclusão cancelada.")
        return


if realizar_login():
    while True:
        escolha = realizar_menu()
        if escolha == "1":
            realizar_saque()
        elif escolha == "2":
            realizar_deposito()
        elif escolha == "3":
            realizar_extrato()
        elif escolha == "4":
            realizar_pix()
        elif escolha == "5":
            if not trocar_usuario():
                print("Encerrando o programa.")
                break
        elif escolha == "6":
            cadastrar_usuario()
        elif escolha == "7":
            consultar_saldo()
        elif escolha == "8":
            excluir_usuario()
        elif escolha == "9":
            realizar_sair()
            print("Encerrando o programa.")
            break
        else:
            print("Opção inválida.")
