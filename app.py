
from flask import Flask, render_template, url_for

app = Flask(__name__)

# Rota para a página principal
@app.route('/')
def index():
    return render_template('index.html')

# Ponto de entrada para o servidor Flask
if __name__ == '__main__':
    app.run(debug=True)
