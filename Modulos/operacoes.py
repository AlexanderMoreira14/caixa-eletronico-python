from datetime import datetime
from Modulos.utilidades import limpar_terminal, ler_valor
from Modulos.dados import salvar_dados, usuario_logado, usuarios

def realizar_saque(usuario):
    hora_atual = datetime.now()
    limpar_terminal()
    
    saque = ler_valor("Digite o valor do saque ou SAIR para voltar: ")
    if saque is None:
        return
    
    if saque <= usuario['saldo']:
        usuario["saldo"] -= saque
        usuario["historico"].append(f"{hora_atual.strftime('%H:%M em %d/%m/%Y')}\nSaque: {saque:.2f}")
        salvar_dados()
        print(f"O saque no valor de R$ {saque:.2f} foi realizado")
        print(f"Seu saldo atual é de R$ {usuario['saldo']:.2f}")
        
    else:
        print("Saldo insuficiente ou valor inválido.")
        return

def realizar_deposito(usuario):
    hora_atual = datetime.now()
    limpar_terminal()

    deposito = ler_valor("Digite o valor do deposito ou SAIR para voltar: ")
    if deposito is None:
        return
    
    if deposito > 0:
        usuario["saldo"] += deposito
        usuario["historico"].append(f"{hora_atual.strftime('%H:%M em %d/%m/%Y')}\nDepósito: +R$ {deposito:.2f}")
        salvar_dados()
        print(f"O depósito no valor de R$ {deposito:.2f} foi feito com sucesso")
        print(f"Seu saldo atual é de R$ {usuario['saldo']:.2f}")
        
    else:
        print("Valor inválido.")

def realizar_extrato(usuario):
    limpar_terminal()
    print(f"\n------ Extrato de {usuario ['login']} ------")
    if not usuario["historico"]:
        print("Nenhuma operação realizada.")
    else: 
        for operacao in usuario["historico"]:
            print(operacao)    
    print(f"Saldo: -R$ {usuario['saldo']:.2f}")
    print("=======================")

def realizar_pix(usuario):
    hora_atual = datetime.now()
    limpar_terminal()
    destino = input("Digite SAIR para voltar ou \nDigite o login do usuário para transferir: ")
    if destino.upper() == "SAIR":
        return
    valor = float (input("Digite o valor do pix: "))
 
    for usuario_destino in usuarios:
        if usuario_destino["login"] == destino.upper():
            
            if usuario_destino == usuario_logado:
                print ("Você não pode fazer PIX para a própria conta.")
                return
            
            if valor > 0 and valor <= usuario_logado["saldo"]:
                usuario["saldo"] -= valor
                usuario_destino["saldo"] += valor
                usuario["historico"].append(f"{hora_atual.strftime('%H:%M em %d/%m/%Y')}\nTransferência realizada para {destino.upper()}: -R$ {valor:.2f}")
                usuario_destino["historico"].append(f"{hora_atual.strftime('%H:%M em %d/%m/%Y')}\nTransferência recebida de {usuario['login']}: +R$ {valor:.2f}")
                salvar_dados()
                print(f"Transferência de R$ {valor:.2f} para {destino.upper()} realizada com sucesso.")
                return
            
            else:
                print("Saldo insuficiente ou valor inválido.")
                return
            
    print("Este usuário não existe")
        
def consultar_saldo(usuario):
    limpar_terminal()
    print(f"Seu saldo atual é de R$ {usuario['saldo']:.2f}")