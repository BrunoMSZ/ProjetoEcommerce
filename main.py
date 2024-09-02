from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from mysql.connector import Error

class Database:
    def __init__(self):
        self.conexao = None
        try:
            self.conexao = mysql.connector.connect(
                host='localhost',
                database='amazon_clone',
                user='root',
                password='root753'
            )
            if self.conexao.is_connected():
                db_info = self.conexao.get_server_info()
                print("Conectado ao serviço MYSQL versão ", db_info)
                cursor = self.conexao.cursor()
                cursor.execute("SELECT DATABASE();")
                amazonClone = cursor.fetchone()
                print("Conectado ao banco de dados", amazonClone)
        except Error as e:
            print("Erro ao conectar ao MYSQL", e)

    def fecha(self):
        if self.conexao and self.conexao.is_connected():
            self.conexao.close()
            print("Conexão ao MYSQL encerrada")

    def inserirDadosClientes(self, nome, email, senha, data_nasc):
        if self.conexao and self.conexao.is_connected():
            cursor = self.conexao.cursor()
            sql_insert = "INSERT INTO Cliente (nomeCompleto, email, dataNascimento, senha) VALUES (%s, %s, %s, %s)"
            values = (nome, email, data_nasc, senha)
            cursor.execute(sql_insert, values)
            self.conexao.commit()
            print(f"{nome} registrado com sucesso!")

    def listarClientes(self):
        if self.conexao and self.conexao.is_connected():
            cursor = self.conexao.cursor()
            cursor.execute("SELECT * FROM Cliente;")
            registros = cursor.fetchall()
            print("Total de clientes registrados: ", cursor.rowcount)
            for linha in registros:
                print("id: ", linha[0], "nome: ", linha[1], "email: ", linha[2])
            return registros
    
    def autentificar(self, email, senha):
        if self.conexao and self.conexao.is_connected():
            cursor = self.conexao.cursor()
            cursor.execute("SELECT idCadastroCliente FROM Cliente WHERE email = %s AND senha = %s", (email, senha))
            result = cursor.fetchall()
            if len(result) > 0:
                return True
            else:
                return False

class Cliente:
    def __init__(self, nome: str, email: str, dataNasc: str, senha: str) -> None:
        self.__id: int = None
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
        db.inserirDadosClientes(nome, email, senha, data_nascimento)
        print(f"Cadastro realizado {nome}")
        db.fecha()
        return f'Welcome, {nome}'
    return render_template('formulario.html')

@app.route('/login', methods=['POST'])
def loginInicial():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')
        db = Database()
        requestAut = db.autentificar(email, senha)
        db.fecha()
        if requestAut:
            print("Login Successful")
            return redirect(url_for('inicio'))
        else:
            return 'Login Failed', 401

if __name__ == "__main__":
    app.run(debug=True)
