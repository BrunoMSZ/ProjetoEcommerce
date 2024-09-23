
from flask import Flask, render_template, request, redirect, url_for, jsonify
import main as m

app = Flask(__name__)

# Rota para a página principal
@app.route('/')
def index():
    db = m.Database()  # Inicializa a conexão com o banco de dados
    produtos = db.listarProdutosPorIds([6, 7, 8])  # Obtém a lista de produtos
    db.fecha()  # Fecha a conexão com o banco de dados
    return render_template('index.html', produtos=produtos)  # Passa a lista de produtos para o template


@app.route('/login', methods=['GET','POST'])
def loginInicial():
    mensagem = request.args.get('mensagem')  # Pega a mensagem da URL
    
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')
        print(email,senha)
        db = m.Database()
        requestAut = db.autentificar(email, senha)
        print("passou!")
        print(requestAut)
        db.fecha()
        if requestAut:
            print("Login Successful")
            return redirect(url_for('loginInicial'))
        else:
            return 'Login Failed', 401
    
    return redirect(url_for('index', mensagem=mensagem))

@app.route('/finalizarCompra', methods=['POST'])
def finalizarCompra():
    data = request.get_json()
    tipo_pagamento = data.get('tipoPagamento')
    valor_pago = data.get('valorPago')
    pedido_id = 1  # Substitua pelo ID real do pedido, você pode gerenciá-lo conforme sua lógica

    db = m.Database()  # Cria uma instância do banco de dados

    # Chama o método para inserir os dados de pagamento
    if db.inserirDadosPagamento(tipo_pagamento, valor_pago, pedido_id):
        return jsonify(success=True)
    else:
        return jsonify(success=False)

@app.route('/register', methods=['POST'])
def register():
    nome = request.form['name']
    email = request.form['email']
    senha = request.form['senha']
    data_nasc = request.form['data_nasc']
    
    # Inserir dados no banco de dados
    db = m.Database()
    db.inserirDadosClientes(nome, email, senha, data_nasc)
    db.fecha()
    
    # Retornar uma mensagem de sucesso e abrir o popup de login
    return redirect(url_for('index'))





# Ponto de entrada para o servidor Flask
if __name__ == '__main__':
    app.run(debug=True)
