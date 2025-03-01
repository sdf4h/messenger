from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Message(BaseModel):
    text: str
    encrypted_key: str
    signature: str

@app.post("/send_message/")
async def send_message(message: Message):
    # Пример обработки сообщения
    user_public_key = ...  # Получение публичного ключа получателя
    private_key = ...  # Получение приватного ключа отправителя

    # Проверка подписи
    if not verify_signature(user_public_key, message.text, message.signature):
        return {"error": "Signature verification failed"}

    # Расшифровка ключа AES
    aes_key = decrypt_aes_key(private_key, message.encrypted_key)
    
    # Расшифровка сообщения
    decrypted_message = decrypt_message_aes(message.text, aes_key)
    return {"decrypted_message": decrypted_message}
