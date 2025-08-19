from flask import Flask, jsonify, request, send_file, render_template
from repository.database import db
from db_models.payments import Payment
from datetime import datetime, timedelta
from payments.pix import PixPayment

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///payments.db' # URI do banco de dados
app.config['SECRET_KEY'] = 'SECRET_KEY' # Chave secreta para criptografia

db.init_app(app)

# Rota para criar um pagamento via PIX
@app.route('/payments/pix', methods=['POST'])
def create_pix_payment():
    
    data = request.get_json()

    # Validacoes para criacao de pagamento
    if 'value' not in data:
        return jsonify({"message": "Dados inválidos"}), 400

    # Data de expiração soma-se mais um dia 
    expiration_date = datetime.now() + timedelta(days=1)

    # Criação do objeto de pagamento
    new_payment = Payment(
        value=data['value'],
        expiration_date=expiration_date
    )

    # Criação do objeto de pagamento PIX
    pix_obj = PixPayment()
    data_payment_pix = pix_obj.create_payment()

    new_payment.bank_payment_id = data_payment_pix['payment_bank_id'] # Atribuição do ID do pagamento bancário
    new_payment.qr_code = data_payment_pix['qr_code_path'] # Atribuição do caminho do QR Code

    db.session.add(new_payment)
    db.session.commit()

    return jsonify(
        {"message": "Pagamento PIX criado com sucesso!", 
         "payment": new_payment.to_dict()
        })

# Rota para devolver a imagem do qr code para o usuario
@app.route('/payments/pix/qr_code/<file_name>', methods=['GET'])
def get_qr_code(file_name):
    return send_file(f'static/img/{file_name}.png', mimetype='image/png')

# Rota para gerar confirmação do pix para pagamento
@app.route('/payments/pix/confirmation', methods=['POST'])
def get_pix_confirmation():
    return jsonify({"message": "Confirmação do pagamento PIX gerada com sucesso!"}), 200

# Rota para visualizar o status do pagamento PIX
@app.route('/payments/pix/<int:payment_id>', methods=['GET'])
def payment_pix_page(payment_id):
    payment = Payment.query.get(payment_id)  # Verifica se o pagamento existe

    return render_template('payment.html', 
                           payment_id=payment_id, 
                           value=payment.value, 
                           host='http://127.0.0.1:5000', 
                           qr_code=payment.qr_code)


if __name__ == '__main__':
    app.run(debug=True)