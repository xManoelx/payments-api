import sys
sys.path.append("../")

import pytest
import os
from payments.pix import PixPayment

def test_create_payment():
    pix_instance = PixPayment()

    # Criar um pagamento
    payment_info = pix_instance.create_payment(base_dir="../")

    assert 'payment_bank_id' in payment_info
    assert 'qr_code_path' in payment_info

    # Verifica se o QR Code foi gerado
    qr_code_path = payment_info['qr_code_path']
    assert os.path.isfile(f"../static/img/{qr_code_path}.png")