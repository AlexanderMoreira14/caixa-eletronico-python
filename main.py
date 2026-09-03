from datetime import datetime
from Modulos.dados import usuarios, salvar_dados
from Modulos.utilidades import limpar_terminal, ler_valor
from Modulos.usuarios import (realizar_login, trocar_usuario,cadastrar_usuario, excluir_usuario, alterar_senha)



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

def realizar_sair():
    limpar_terminal()
    print("Você saiu do caixa. Até logo!")

usuario_logado = realizar_login()
if usuario_logado:
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
                novo_usuario = trocar_usuario()
                if novo_usuario:
                    usuario_logado = novo_usuario
                else:
                    print("Não foi possível trocar de usuário. Encerrando o programa.")
    
            case "6":
                usuario_atualizado = cadastrar_usuario()
                if usuario_atualizado:
                    usuario_logado = usuario_atualizado
            case "7":
                consultar_saldo()
            case "8":
                if excluir_usuario(usuario_logado):
                    usuario_logado = realizar_login()
            case "9":
                alterar_senha(usuario_logado)
            case "10":
                realizar_sair()
                print("Encerrando o programa.")
                break
            case _:
                print("Opção inválida.")
