from Modulos.dados import usuarios, salvar_dados, registrar_novo_usuario, remover_usuario_banco, atualizar_senha_banco
from Modulos.utilidades import limpar_terminal, ler_valor

def realizar_login():
    tentativas = 0
    
    while tentativas < 3:
        tentativas += 1
        login_input = input("Digite o seu login: ")
        senha_input = input("Digite a sua senha: ")
        
        for usuario in usuarios:
            if login_input.upper() == usuario["login"] and senha_input == usuario["senha"]:
                print(f"\nBem-vindo, {usuario['login']}!")
                return usuario
        else:
            print(f"Login ou senha incorretos. Tentativas restantes: {3 - tentativas}")                       
    print("Conta bloqueada.")
    return None

def trocar_usuario():
    limpar_terminal()

    novo_usuario = realizar_login()
    return novo_usuario

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
    
    registrar_novo_usuario(cadastro_novo, cadastro_senha)
    
    print(f"Usuário {cadastro_novo} cadastrado com sucesso!")
    return realizar_login()

def excluir_usuario(usuario_logado):    
    limpar_terminal()
    confirmacao = input(f"Tem certeza que deseja excluir o usuário {usuario_logado['login']}?\n Digite apenas SIM ou NÃO: ").upper()
    if confirmacao == "SIM":
        tentativas = 0
        while tentativas < 3:
            tentativas += 1
            senha_confirmacao = input("Digite a senha do usuário para confirmar a exclusão: ")
            
            if senha_confirmacao == usuario_logado['senha']:
                usuarios.remove(usuario_logado)
                remover_usuario_banco(usuario_logado['login'])
                salvar_dados()
                print(f"Usuário {usuario_logado['login']} excluído com sucesso.")
                usuario_logado = None
                return True
            else:   
                print(f"Senha incorreta. Tentativas restantes: {3 - tentativas}")
            if tentativas == 3:
                print("Número máximo de tentativas atingido. Exclusão cancelada.")
                return False
    else:
        print("Exclusão cancelada.")
        return False

def alterar_senha(usuario_logado):
    senha_atual = input("Digite a senha atual: ")
    
    if senha_atual == usuario_logado['senha']:
        senha_nova = input("Digite a nova senha: ")
        confirmar_senha = input("Confirme a nova senha: ")
        
        if confirmar_senha == senha_nova:
            usuario_logado['senha'] = senha_nova
            atualizar_senha_banco(usuario_logado['login'], senha_nova)
            print("Senha alterada com sucesso.")
        else:
            print("Senhas diferentes. Alteração cancelada")   
        return
    else:
        print("Senha incorreta.")
        


