from datetime import datetime
import json
import os


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

def limpar_terminal():
    os.system("cls")
    
def ler_valor(mensagem):
    while True:
        entrada = input(mensagem)
        
        if entrada.upper() == "SAIR":
            return None
        
        try:
            valor = float(entrada)

            if valor > 0:
                return valor

            print("O valor precisa ser maior que zero.")

        except ValueError:
            print("Digite um número válido ou SAIR.")
    
    
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
    print("7 - Consultar Saldo")
    print("8 - Excluir usuário")
    print("9 - Alterar senha")
    print("10 - Sair do programa")
    return input("Escolha uma opção: ")
    
def realizar_saque():
    hora_atual = datetime.now()
    limpar_terminal()
    
    saque = ler_valor("Digite o valor do saque ou SAIR para voltar: ")
    if saque is None:
        return
    
    if saque <= usuario_logado['saldo']:
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
    limpar_terminal()

    deposito = ler_valor("Digite o valor do deposito ou SAIR para voltar: ")
    if deposito is None:
        return
    
    if deposito > 0:
        usuario_logado["saldo"] += deposito
        usuario_logado["historico"].append(f"{hora_atual.strftime('%H:%M em %d/%m/%Y')}\nDepósito: +R$ {deposito:.2f}")
        salvar_dados()
        print(f"O depósito no valor de R$ {deposito:.2f} foi feito com sucesso")
        print(f"Seu saldo atual é de R$ {usuario_logado['saldo']:.2f}")
        
    else:
        print("Valor inválido.")

def realizar_extrato():
    limpar_terminal()
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
    limpar_terminal()
    destino = input("Digite SAIR para voltar ou \nDigite o login do usuário para transferir: ")
    if destino.upper() == "SAIR":
        return
    valor = float (input("Digite o valor do pix: "))
 
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
    limpar_terminal()
    print(f"Seu saldo atual é de R$ {usuario_logado['saldo']:.2f}")
    
def trocar_usuario():
    global usuario_logado
    usuario_logado = None
    if realizar_login():
        return True
    else:
        return False

def realizar_sair():
    limpar_terminal()
    print("Você saiu do caixa. Até logo!")

def cadastrar_usuario():
    limpar_terminal()
    cadastro_novo = input("Digite SAIR para voltar. \nDigite novo usuário: ").upper().strip()
    if cadastro_novo == "SAIR":
        return
    
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
    limpar_terminal()
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

def alterar_senha():
    senha_atual = input("Digite a senha atual: ")
    if senha_atual == usuario_logado['senha']:
        senha_nova = input("Digite a nova senha: ")
        usuario_logado['senha'] = senha_nova
        salvar_dados()
        print("Senha alterada com sucesso.")
    else:
        print("Senha incorreta.")



if realizar_login():
    while True:

        escolha = realizar_menu()

        match escolha:

            case "1":
                realizar_saque()
            case "2":
                realizar_deposito()
            case "3":
                realizar_extrato()
            case "4":
                realizar_pix()
            case "5":
                if not trocar_usuario():
                    print("Encerrando o programa.")
                break
            case "6":
                cadastrar_usuario()
            case "7":
                consultar_saldo()
            case "8":
                excluir_usuario()
            case "9":
                alterar_senha()
            case "10":
                realizar_sair()
                print("Encerrando o programa.")
                break
            case _:
                print("Opção inválida.")
