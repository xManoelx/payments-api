import uuid
import qrcode

class PixPayment:
    def __init__(self):
        pass

    def create_payment(self):
        # Cria o pagamento na instituição financeira
        bank_payment_id = str(uuid.uuid4()) # Simula uma instituição financeira

        # Código copia e cola
        hash_payment = f'hash_payment_{bank_payment_id}'
        
        # QR Code
        img = qrcode.make(hash_payment)

        # Salva a imagem do QR Code em PNG
        img.save(f'static/img/qr_code_payment_{bank_payment_id}.png')

        return {'payment_bank_id': bank_payment_id,
                'qr_code_path': f'qr_code_payment_{bank_payment_id}'}
