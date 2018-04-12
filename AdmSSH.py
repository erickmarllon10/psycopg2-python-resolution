from Usuarios.Usuarios import cadastrar_usuario, acessar_sistema, alterar_senha, listar_admin, sair
from Servidores.Servidores import cadastrar_servidor, remover_servidor, definir_admin

def menu():
    print "\
            1 - Cadastrar Usuario: \n\
            2 - Acessar Sistema: \n\
            3 - Cadastrar Servidor: \n\
            4 - Remover Servidor: \n\
            5 - Definir Administrador: \n\
            6 - Alterar Senha: \n\
            7 - Sair: \n"

    option = input("Escolha a opcao desejada: ")
    return option

def switch(x):
    dict_options = {1:cadastrar_usuario,2:acessar_sistema,3:cadastrar_servidor,4:remover_servidor,5:definir_admin,6:alterar_senha,7:sair}
    dict_options[x]()

if __name__ == '__main__':
    while True:
        switch(menu())
