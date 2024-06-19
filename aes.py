from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.backends import default_backend
import os

folder = './test/'


def generate_aes_key():
    key = AESGCM.generate_key(bit_length=256)  # 256-bit key
    return key


def encrypt_file_aes(key, input_file, output_file):
    iv = os.urandom(16)  # Initialization vector
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv),
                    backend=default_backend())
    encryptor = cipher.encryptor()

    with open(folder + input_file, 'rb') as f:
        plaintext = f.read()

    ciphertext = encryptor.update(plaintext) + encryptor.finalize()

    with open(folder + output_file, 'wb') as f:
        f.write(iv + ciphertext)


def decrypt_file_aes(key, input_file, output_file):
    with open(folder + input_file, 'rb') as f:
        iv = f.read(16)
        ciphertext = f.read()

    cipher = Cipher(algorithms.AES(key), modes.CFB(iv),
                    backend=default_backend())
    decryptor = cipher.decryptor()

    plaintext = decryptor.update(ciphertext) + decryptor.finalize()

    with open(folder + output_file, 'wb') as f:
        f.write(plaintext)
