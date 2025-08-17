from flask import Flask, jsonify
from repository.database import db
from db_models.payments import Payment

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///payments.db' # URI do banco de dados
app.config['SECRET_KEY'] = 'SECRET_KEY' # Chave secreta para criptografia

db.init_app(app)

# Rota para criar um pagamento via PIX
@app.route('/payments/pix', methods=['POST'])
def create_pix_payment():
    # Lógica para criar um pagamento via PIX
    return jsonify({"message": "Pagamento PIX criado com sucesso!"}), 201

# Rota para gerar confirmação do pix para pagamento
@app.route('/payments/pix/confirmation', methods=['POST'])
def get_pix_confirmation():
    return jsonify({"message": "Confirmação do pagamento PIX gerada com sucesso!"}), 200

# Rota para visualizar o status do pagamento PIX
@app.route('/payments/pix/<int:payment_id>', methods=['GET'])
def payment_pix_page(payment_id):
    return 'pagamento pix'


if __name__ == '__main__':
    app.run(debug=True)