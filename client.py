import socket
import threading
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

HOST = '127.0.0.1'
PORT = 12345

key = b'1234567890123456'  # 16-byte key

def encrypt_message(message):
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.encrypt(pad(message.encode(), 16))

def decrypt_message(message):
    cipher = AES.new(key, AES.MODE_ECB)
    return unpad(cipher.decrypt(message), 16).decode()

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

def receive():
    while True:
        try:
            message = client.recv(1024)
            print("Received:", decrypt_message(message))
        except:
            print("Error!")
            client.close()
            break

def write():
    while True:
        msg = input("")
        encrypted = encrypt_message(msg)
        client.send(encrypted)

threading.Thread(target=receive).start()
threading.Thread(target=write).start()