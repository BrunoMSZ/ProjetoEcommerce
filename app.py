
from flask import Flask, render_template, request, redirect, url_for, jsonify
import main as m

app = Flask(__name__)

# Rota para a página principal
@app.route('/')
def index():
    db = m.Database()
    produtos = db.listarProdutosPorIds([6, 7, 8])
    db.fecha()
    return render_template('index.html', produtos=produtos)


@app.route('/login', methods=['GET','POST'])
def loginInicial():
    mensagem = request.args.get('mensagem')
    
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
    pedido_id = 1
    db = m.Database()
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
    db = m.Database()
    db.inserirDadosClientes(nome, email, senha, data_nasc)
    db.fecha()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
