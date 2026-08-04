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
    print("Conta bloqueada MANO VEIO IMBECIL.")
    return False

def realizar_menu():
    print("\n---- MENU BANCO ----")
    print("1 - Saque")
    print("2 - Depositar")
    print("3 - Extrato")
    print("4 - PIX")
    print("5 - Trocar de Usuário")
    print("6 - Sair")
    print("7 - Saldo")
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
        return realizar_saque()

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
    print("\n------ Extrato ------")
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
                print("Muito burro. Encerrando o programa.")
                break
        elif escolha == "6":
            realizar_sair()
            break
        elif escolha == "7":
            consultar_saldo()
        else:
            print("Opção inválida.")
