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

app = Flask(__name__)

@app.route('/')
def inicio():
    db = Database()
    produtos = db.listarProdutos()  # Busca os produtos do banco de dados
    db.fecha()
    return render_template('mainPrincipal.html', produtos=produtos)


@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        data_nascimento = request.form['dataNascimento']
        
        # Conectar ao banco de dados
        db = Database()
        # Inserir dados do cliente
        db.inserirDadosClientes(nome, email, str(senha), data_nascimento)
        db.fecha()
        
        # Redirecionar para a página de login com uma mensagem de sucesso
        return redirect(url_for('loginInicial', mensagem='Cadastro bem-sucedido!'))
    
    return render_template('cadastroUsuario.html')


@app.route('/login', methods=['GET','POST'])
def loginInicial():
    mensagem = request.args.get('mensagem')  # Pega a mensagem da URL
    
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')
        print(email,senha)
        db = Database()
        requestAut = db.autentificar(email, senha)
        print("passou!")
        print(requestAut)
        db.fecha()
        if requestAut:
            print("Login Successful")
            return redirect(url_for('inicio'))
        else:
            return 'Login Failed', 401
    
    return render_template('login.html', mensagem=mensagem)


@app.route('/cadastroProduto', methods=['GET', 'POST'])
def cadastroItem():
    if request.method == 'POST':
        nome = request.form.get('nome')
        descricao = request.form.get('descricao')
        preco = request.form.get('preco')
        estoque = request.form.get('estoque')
        categoriaId = request.form.get('categoriaId')
        itemPedidoId = request.form.get('itemPedidoId')
        cor = request.form.get('cor')
        voltagem = request.form.get('voltagem')
        comentario = request.form.get('comentario')
        dimensao = request.form.get('dimensao')
        db = Database()
        db.inserirDadosProduto(nome, descricao, preco, estoque, categoriaId, itemPedidoId, cor, voltagem, comentario, dimensao)
        db.fecha()
        print("Cadastro de Produto bem-sucedido")
        return redirect(url_for('inicio'))
    return render_template('cadastroProduto.html')

@app.route('/finalizar_compra', methods=['POST'])
def finalizar_compra():
    data = request.json

    tipo_pagamento = data.get('metodo_pagamento')
    itens = data.get('itens', [])
    
    # Verifique se 'itens' não está vazio
    if not itens:
        return jsonify({'message': 'Nenhum item no carrinho!'}), 400
    
    # Calcular o total dos itens
    valor_pago = sum(item['price'] for item in itens if 'price' in item)
    
    pedido_id = data.get('pedido_id')  # Supondo que você forneça o ID do pedido
    data_pagamento = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Data e hora atual

    db = Database()  # Criar uma instância da classe Database
    try:
        cursor = db.conexao.cursor()
        # Inserir dados na tabela dadosPagamento
        cursor.execute(
            "INSERT INTO dadosPagamento (dataPagamento, tipoPagamento, statusPago, valorPago, Pedido_idPedido) VALUES (%s, %s, %s, %s, %s)",
            (data_pagamento, tipo_pagamento, 1, valor_pago, pedido_id)  # Corrigido para 'Pago'
        )
        db.conexao.commit()  # Confirmar a transação
        return jsonify({'message': 'Compra finalizada com sucesso!'}), 201
    except Error as e:
        print("Erro ao finalizar a compra", e)
        return jsonify({'message': 'Erro ao finalizar a compra'}), 500
    finally:
        db.fecha()  # Garantir que a conexão seja fechada


@app.route('/finalizarCompra')
def finalizar_compra_page():
    return render_template('finalizarCompra.html')

@app.route('/carrinho', methods=['GET', 'POST'])
def mostrarCarrinho():
    return render_template('carrinho.html')

@app.route('/contact', methods=['GET', 'POST'])
def contato():
    return render_template('contato.html')

if __name__ == "__main__":
    app.run(debug=True)
