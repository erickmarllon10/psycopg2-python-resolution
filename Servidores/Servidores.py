import sys
import psycopg2
from Usuarios.Usuarios import listar_admin

def cadastrar_servidor():
    print "------------------------------------"
    print "------ Cadastro de Servidores ------"
    print "------------------------------------"
    ip = raw_input ("Digite o endereco IP do servidor: ")
    serverName = raw_input ("Digite o nome do servidor: ")
    admLogin = raw_input ("Digite o nome do Sysadmin: ")

    try:
        con = psycopg2.connect("host=127.0.0.1 dbname=onxenti user=onxentiadmin password=123456")
        cur = con.cursor()
        sql = "insert into servers(endereco,nome,sysadmin) values(%s, %s, %s)"
        sql_data = (ip, serverName, admLogin)
        cur.execute (sql, sql_data)
	con.commit()
	print "Servidor %s de ip %s cadastrado com sucesso"%(serverName, ip)
    except Exception as e:
        print "Erro: %s"%e
        con.rollback()
    finally:
        cur.close()
        con.close()

def remover_servidor():
    print "Removendo servidor"
    try:
        con = psycopg2.connect("host=127.0.0.1 dbname=onxenti user=onxentiadmin password=123456")
        cur = con.cursor()
        cur.execute("select * from servers")
        for s in (cur.fetchall()):
            print "Server:",s[2], "ID:",s[0], "IP:",s[1]
        option = raw_input("Escolha o id do servidor que deseja remover: ")
        sql = "select * from servers where id = (%s)"
        cur.execute(sql, option)
        servidor = cur.fetchone()
        opt = raw_input("Tem certeza que deseja remover o servidor %s? (s ou n): "%servidor[2])
        if opt == 's':
            sql_data = "delete from servers where id = (%s)"
            cur.execute(sql_data, option)
            con.commit()
            print "Servidor %s removido"%servidor[2]
        else:
            print "Ufa! voce salvou o servidor %s"%servidor[2]
    except Exception as e:
        print "Erro: "%e
    finally:
        cur.close()
        con.close()

def definir_admin():
    listar_admin()
    option = raw_input("Digite o nome do admin ou s para sair: ")
    if option == 's':
        print "saindo"
        sys.exit()    
    else:
        con = psycopg2.connect("host=127.0.0.1 dbname=onxenti user=onxentiadmin password=123456")
        cur = con.cursor()
        cur.execute("select login_access from users where login_access = '%s'"%option)
        usuario = cur.fetchone()
        print "Voce selecionou o usuario %s"%usuario
        defAdm = raw_input("Deseja selecionar um servidor para este usuario? (s ou n):")
        if defAdm == 's':
            cur.execute("select * from servers")
            for s in cur.fetchall():
                print "Id: ",s[0],"Endereco:",s[1],"Nome:",s[2],"Adm Atual:",s[3]
                while True:
                    choose = input("Digite o id do servidor: ")
   
                    if choose not in s:
                        print "Id invalido"
                    else:
                        break
                sql2 = "update servers set sysadmin = (%s) where id = (%s)"
                data = (usuario, choose)
                cur.execute(sql2, data)
                con.commit()
                print "Administrador %s definido com sucesso"%usuario
                cur.execute("select * from servers")
                for s in cur.fetchall():
                    print "Nome:",s[2],"Novo Adm:",s[3]
                break

        else:
            print "Ops, parece que voce dedistiu!"

