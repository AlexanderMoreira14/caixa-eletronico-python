from datetime import datetime
from Modulos.dados import usuarios, salvar_dados
from Modulos.utilidades import limpar_terminal, ler_valor
from Modulos.usuarios import (realizar_login, trocar_usuario,cadastrar_usuario, excluir_usuario, alterar_senha)
from Modulos.operacoes import (realizar_saque, realizar_deposito, realizar_extrato, realizar_pix, consultar_saldo)


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
    
def realizar_sair():
    limpar_terminal()
    print("Você saiu do caixa. Até logo!")

usuario_logado = realizar_login()
if usuario_logado:
    while True:

        escolha = realizar_menu()

        match escolha:

            case "1":
                realizar_saque(usuario_logado)
            case "2":
                realizar_deposito(usuario_logado)
            case "3":
                realizar_extrato(usuario_logado)
            case "4":
                realizar_pix(usuario_logado)
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
                consultar_saldo(usuario_logado)
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
