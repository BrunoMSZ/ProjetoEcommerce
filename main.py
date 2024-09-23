from flask import Flask, render_template, request, redirect, url_for,jsonify
import mysql.connector
from mysql.connector import Error
from datetime import datetime

class Database:
    def __init__(self):
        self.conexao = None
        try:
            self.conexao = mysql.connector.connect(
                host='127.0.0.1',
                user='root',
                password='123456',
                database='amazon_clone'
            )
            if self.conexao.is_connected():
                db_info = self.conexao.get_server_info()
                print("Conectado ao serviço MYSQL versão", db_info)
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
            try:
                cursor = self.conexao.cursor()
                #hashed_password = generate_password_hash(senha)
                sql_insert = "INSERT INTO Cliente (nomeCompleto, email, dataNascimento, senha) VALUES (%s, %s, %s, %s)"
                values = (nome, email, data_nasc, senha)
                #print(hashed_password)
                cursor.execute(sql_insert, values)
                self.conexao.commit()
                print(f"{nome} registrado com sucesso!")
            except Error as e:
                print("Erro ao inserir dados do cliente", e)

    def listarClientes(self):
        if self.conexao and self.conexao.is_connected():
            try:
                cursor = self.conexao.cursor()
                cursor.execute("SELECT * FROM Cliente;")
                registros = cursor.fetchall()
                print("Total de clientes registrados:", cursor.rowcount)
                for linha in registros:
                    print("id:", linha[0], "nome:", linha[1], "email:", linha[2])
                return registros
            except Error as e:
                print("Erro ao listar clientes", e)
                return []

    def autentificar(self, email, senha):
        if self.conexao and self.conexao.is_connected():
            try:
                cursor = self.conexao.cursor()
                cursor.execute("SELECT senha FROM Cliente WHERE email = %s", (email,))
                result = cursor.fetchone()
                if result:
                    stored_password = result[0]  # Access the password using index 0
                    print(stored_password)
                    if stored_password == senha:
                        return True
                return False
            except Error as e:
                print("Erro ao autenticar usuário", e)
                return False

    def inserirDadosProduto(self, nome, descricao, preco, estoque, categoriaId, itemPedidoId, cor, voltagem, comentario, dimensao):
        if self.conexao and self.conexao.is_connected():
            try:
                cursor = self.conexao.cursor()
                # Verificar se a categoria existe
                cursor.execute("SELECT COUNT(*) FROM categoria WHERE idCategoria = %s", (categoriaId,))
                categoria_existe = cursor.fetchone()[0]
                
                if categoria_existe == 0:
                    print(f"Categoria com id {categoriaId} não encontrada.")
                    return False

                sql_insert = """
                    INSERT INTO produto (nome, descricao, preco, estoque, Categoria_idCategoria, ItemPedido_idItemPedido, cor, voltagem, comentario, dimensao)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                values = (nome, descricao, preco, estoque, categoriaId, itemPedidoId, cor, voltagem, comentario, dimensao)
                cursor.execute(sql_insert, values)
                self.conexao.commit()
                print(f"Produto {nome} registrado com sucesso!")
                return True
            except Error as e:
                print("Erro ao inserir dados do produto", e)
                return False

    def listarProdutos(self):
        if self.conexao and self.conexao.is_connected():
            try:
                cursor = self.conexao.cursor()
                cursor.execute("SELECT nome, descricao, preco, imagem_url FROM Produto;")  # Ajuste conforme sua tabela
                registros = cursor.fetchall()
                return [{'nome': linha[0], 'descricao': linha[1], 'preco': linha[2], 'imagem_url': linha[3]} for linha in registros]
            except Error as e:
                print("Erro ao listar produtos", e)
                return []

    

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
