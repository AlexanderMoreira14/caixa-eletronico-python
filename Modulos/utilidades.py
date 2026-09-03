import os

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