import psycopg2
import sys

def cadastrar_usuario():
    print "Cadastro de usuarios"
    nome = raw_input("Cadastre o nome do usuario: ")
    while True:
        senha = raw_input("Cadastre a senha do usuario %s: "%nome)
        senhaconf = raw_input("Digite a senha novamente: ")
        if senhaconf != senha:
            print "As senhas nao coincidem"
        else:
            break
    try:
        con = psycopg2.connect("host=127.0.0.1 dbname=onxenti user=onxentiadmin password=123456")
        cur = con.cursor()
        sql = "insert into users(login_access,passwd) values(%s, %s)"
        cred = (nome, senha)
        cur.execute(sql, cred)
        con.commit()
        print "Usuario %s cadastrado com sucesso"%nome
    except Exception as e:
        print "Erro: "%e
    finally:
        cur.close()
        con.close()

def acessar_sistema():
    print "Acessando sistema"
    nome = raw_input("Digite o seu login: ")
    senha = raw_input("Digite a sua senha: ")
    try:
        con = psycopg2.connect("host=127.0.0.1 dbname=onxenti user=onxentiadmin password=123456")
        cur = con.cursor()
        cur.execute("select * from users where login_access = '%s'"%nome)
        if cur.fetchone() == None:
            print "Usuario incorreto."
        else:
            cur.execute("select * from users where login_access = '%s' and passwd = '%s'"%(nome, senha))
            count = 1
            while count <=4:
                if cur.fetchone() == None:
                    senha = raw_input("Senha incorreta. Digite novamente ou s para \"esqueci a senha\" (tentativa %s de 3): "%count)
                    if senha == 's':
                        resposta = raw_input("qual o seu local de nascimento? ")
                        if resposta != 'recife':
                            print "Resposta incorreta!"
                        else:
                            cur.execute("select passwd from users where login_access = '%s'"%nome)
                            for l in cur.fetchone():
                                print "Sua senha e",l
                    else:
                        cur.execute("select * from users where login_access = '%s' and passwd = '%s'"%(nome, senha))
                        count += 1
                else:
                    print "Autenticado com sucesso"
                    break

    except Exception as e:
        print "Erro: "%e
    finally:
        cur.close()
        con.close()

def alterar_senha():
    print "Alteracoes de senha"
    nome = raw_input("Digite o seu login: ")
    senha = raw_input("Digite a sua senha atual: ")
    try:
        con = psycopg2.connect("host=127.0.0.1 dbname=onxenti user=onxentiadmin password=123456")
        cur = con.cursor()
        sql = "select * from users where login_access = (%s) and passwd = (%s)"
        save = (nome, senha)
        cur.execute(sql, save)
        if cur.fetchone() == None:
            print "Acesso Negado"
        else:
            while True:
                newPass = raw_input("Digite a nova senha: ")
                newPassConfirm = raw_input("Confirme a nova senha: ")
                if newPassConfirm != newPass:
                    print "As senhas nao coincidem"
                else:
                    break
            sql2 = "update users set passwd = (%s) where login_access = (%s)"
            save2 = (newPass, nome)
            cur.execute(sql2, save2)
            con.commit()
            print "Senha alterada com sucesso"
    except Exception as e:
        print "Erro: "%e
        con.rollback()
    finally:
        cur.close()
        con.close()

def listar_admin():
    try:
        con = psycopg2.connect("host=127.0.0.1 dbname=onxenti user=onxentiadmin password=123456")
        cur = con.cursor()
        sql = "select * from users"
        cur.execute(sql)
        for a in cur.fetchall():
            print "Nome:",a[1]
    except Exception as e:
        print "Erro: "%e

def sair():
    print "Saindo do sistema"
    sys.exit()



