from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

# Подписание сообщения с использованием RSA
def sign_message(private_key, message):
    return private_key.sign(
        message.encode(),
        padding.PKCS1v15(),
        hashes.SHA256()
    )

# Проверка подписи сообщения с использованием публичного ключа
def verify_signature(public_key, message, signature):
    try:
        public_key.verify(
            signature,
            message.encode(),
            padding.PKCS1v15(),
            hashes.SHA256()
        )
        return True
    except:
        return False
