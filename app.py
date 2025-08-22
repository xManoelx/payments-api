from flask import Flask, jsonify, request, send_file, render_template
from repository.database import db
from db_models.payments import Payment
from datetime import datetime, timedelta
from payments.pix import PixPayment
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///payments.db' # URI do banco de dados
app.config['SECRET_KEY'] = 'SECRET_KEY' # Chave secreta para criptografia

db.init_app(app)
socketio = SocketIO(app)

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
    data = request.get_json()

    # Validações para confirmação de pagamento
    if 'bank_payment_id' not in data and 'value' not in data:
        return jsonify({"message": "Dados de pagamento inválidos"}), 400

    # Obtém o pagamento 
    payment = Payment.query.filter_by(bank_payment_id=data.get('bank_payment_id')).first()

    # Validações para existência do pagamento
    if not payment or payment.paid:
        return jsonify({"message": "Pagamento não encontrado"}), 404
    
    # Verifica se o valor de pagamento esta correto
    if data.get('value') != payment.value:
        return jsonify({"message": "Valor de pagamento incorreto"}), 400
    
    payment.paid = True
    db.session.commit()
    socketio.emit(f'payment-confirmed-{payment.id}')
    return jsonify({"message": "Confirmação do pagamento PIX gerada com sucesso!"}), 200

# Rota para visualizar o status do pagamento PIX
@app.route('/payments/pix/<int:payment_id>', methods=['GET'])
def payment_pix_page(payment_id):
    payment = Payment.query.get(payment_id)  # Verifica se o pagamento existe

    if not payment:
        return render_template('404.html'), 404

    if payment.paid:
        return render_template('confirmed_payment.html', 
                               payment_id=payment_id,
                               value=payment.value)

    return render_template('payment.html', 
                           payment_id=payment_id, 
                           value=payment.value, 
                           host='http://127.0.0.1:5000', 
                           qr_code=payment.qr_code)

# Secao websocket
@socketio.on('connect')
def handle_connect():
    print('Cliente conectado')

@socketio.on('disconnect')
def handle_disconnect():
    print('Cliente desconectado')

if __name__ == '__main__':
    socketio.run(app, debug=True)