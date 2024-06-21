from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os


def generate_aes_key():
    return os.urandom(32)  # 256-bit key


def encrypt_file_aes(key, input_file, output_file):
    iv = os.urandom(16)  # Initialization vector
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv),
                    backend=default_backend())
    encryptor = cipher.encryptor()

    with open(input_file, 'rb') as f:
        plaintext = f.read()

    ciphertext = encryptor.update(plaintext) + encryptor.finalize()

    with open(output_file, 'wb') as f:
        f.write(iv + ciphertext)


def decrypt_file_aes(key, input_file, output_file):
    with open(input_file, 'rb') as f:
        iv = f.read(16)  # Initialization vector
        ciphertext = f.read()

    cipher = Cipher(algorithms.AES(key), modes.CFB(iv),
                    backend=default_backend())
    decryptor = cipher.decryptor()

    plaintext = decryptor.update(ciphertext) + decryptor.finalize()

    with open(output_file, 'wb') as f:
        f.write(plaintext)
