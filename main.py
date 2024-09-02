from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from mysql.connector import Error
import classes

class Database:
    conexao = None
    def __init__(self):
        try:
            conexao = mysql.connector.connect(
                host='localhost',
                database='amazon_clone',
                user ='root',
                password='root753'
            )
            if self.conexao.is_connected():
                db_info = self.conexao.get_server_info()
                print("Conectado ao serviço MYSQL versão ", db_info)
                cursor = self.conexao.cursor()
                cursor.execute("select amazon_clone();")
                amazonClone = cursor.fetchone()
                print("Conectado ao banco de dados", amazonClone)
        except Error as e:
            print("Erro ao conectar ao MYSQL", e)

    def fecha(self):
        if self.conexao.is_connected():
            self.conexao.close()
            print("Conexão ao MYSQL encerrada")

    def inserirDadosClientes(self, nome,email,senha,data_nasc):
        if self.conexao.is_connected():
            cursor = self.conexao.cursor()
            sql_insert = "INSERT INTO Cliente (nomeCompleto,email,dataNascimento,senha) VALUES (%s, %s,%s,%s)"
            values=(nome, email, data_nasc, senha)
            cursor.execute(sql_insert, values)
            self.conexao.commit()
            print(f"{clienteCadastro.nome} registrado com sucesso!")

    def listarClientes(self):
        if self.conexao.is_connected():
            cursor = self.conexao.cursor()
            cursor.execute("select * from cliente;")
            registros = cursor.fetchall()
            print("Total de clientes registrados: ", cursor.rowcount)
            for linha in registros:
                print("id: ", linha[0], "nome: ", linha[1], "descrição: ", linha[2])
            return registros
    
    def autentificar(self,email,senha):
        if self.conexao.is_connected():
            print("Conectado ao servidor MYSQL")
            cursor = self.conexao.cursor()
            cursor.execute("SELECT idCadastroCliente from Cliente where email = '",email,"' and senha = '",senha,"';")
            if(cursor.fetchall()!= 0):
                return False
            else:
                return True
    
class Cliente:
    def __init__(self: object, nome: str, email: str, dataNasc: str, senha: str) -> None:
        self.__id: int = id
        self.__nome: str = nome
        self.__email: str = email
        self.__dataNasc: str = dataNasc
        self.__senha: str = senha

    @property
    def id(self):
        return self.__id
    
    @property
    def nome(self):
        return self.__nome
    
    @property
    def email(self):
        return self.__email

    @property
    def dataNasc(self):
        return self.__dataNasc
    
    @property
    def senha(self):
        return self.__senha

app = Flask(__name__)

@app.route('/')
def inicio():
    return render_template('mainPrincipal.html')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        data_nascimento = request.form['dataNascimento']
        db = Database()
        db.inserirDadosClientes(nome,email,senha,data_nascimento)
        print(f"Cadastro realizado {nome}")
        return f'Welcome, {nome}'
    return render_template('formulario.html')
 

"""@app.route('/login', methods=['POST'])
def loginInicial():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')
        db = Database()
        requestAut = db.autentificar(email, senha)
        if requestAut == True:
            print("Login Successful")
        else:
            cadastro()

    return redirect(url_for('inicio'))"""

"""@app.route('/carrinho', methods=['GET', 'POST'])
def carrinhoCompras():
    if Database.conexao.is_connected():
        print("Conectado ao servidor MYSQL")
        account = Database.autentificar(loginInicial.email,loginInicial.senha)
        if(account == False):
            print("Erro ao tentar se conectar a conta!")"""
        

if __name__ == "__main__":
    app.run(debug=True)
    db = Database()
    clienteCadastro = Cliente("CatName","CatDesc")
    db.inserirDadosClientes(clienteCadastro)
    lista = db.listarClientes()
    db.fecha()

    #db.listarClientes()


