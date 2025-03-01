from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os
import base64

# Генерация пары RSA ключей
def generate_rsa_keys():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key = private_key.public_key()
    return private_key, public_key

# Шифрование сообщения с использованием AES
def encrypt_message_aes(plain_text, key):
    iv = os.urandom(16)  # Инициализационный вектор
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    padded_data = plain_text + (16 - len(plain_text) % 16) * ' '  # Паддинг для AES
    cipher_text = encryptor.update(padded_data.encode()) + encryptor.finalize()
    return base64.b64encode(iv + cipher_text).decode()

# Расшифровка сообщения с использованием AES
def decrypt_message_aes(cipher_text, key):
    cipher_text = base64.b64decode(cipher_text)
    iv = cipher_text[:16]
    cipher_text = cipher_text[16:]
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted = decryptor.update(cipher_text) + decryptor.finalize()
    return decrypted.decode().rstrip()

# Шифрование ключа AES с помощью RSA
def encrypt_aes_key(public_key, aes_key):
    cipher_text = public_key.encrypt(
        aes_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return base64.b64encode(cipher_text).decode()

# Расшифровка ключа AES с помощью RSA
def decrypt_aes_key(private_key, encrypted_aes_key):
    encrypted_aes_key = base64.b64decode(encrypted_aes_key)
    aes_key = private_key.decrypt(
        encrypted_aes_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return aes_key
