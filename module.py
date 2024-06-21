import os
import json
import hashlib
import aes
import rsa
from cryptography.hazmat.primitives import serialization


def encrypt_module(filepath, user_name):
    # Bước 2: Hệ thống phát sinh khóa bí mật Ks và mã hóa tập tin P thành tập tin C bằng AES
    aes_key = aes.generate_aes_key()

    # Tạo tên tập tin mã hóa theo định dạng [tên_tập_tin]_encrypt.txt
    file_name, file_extension = os.path.splitext(filepath)
    encrypted_file = f"{file_name}_encrypt{file_extension}"

    aes.encrypt_file_aes(aes_key, filepath, encrypted_file)

    # Bước 3: Hệ thống phát sinh cặp khóa Kprivate và Kpublic của RSA và mã hóa khóa Ks bằng Kpublic
    private_key, public_key = rsa.generate_rsa_key_pair()
    encrypted_key = rsa.encrypt_string_rsa(public_key, aes_key.hex())

    # Bước 4: Hệ thống lưu lại chuỗi Kx kèm theo giá trị hash SHA-1 của Kprivate vào secret.json
    sha1_hash = hashlib.sha1(private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )).hexdigest()

    metadata = {
        user_name: {
            "Kx": encrypted_key.hex(),  # Lưu dưới dạng hex để dễ lưu trữ
            "SHA-1": sha1_hash
        }
    }

    # Đọc secret.json hiện tại nếu có, nếu không thì tạo mới
    secret_file = 'secret.json'
    if os.path.exists(secret_file):
        with open(secret_file, 'r') as f:
            existing_data = json.load(f)
    else:
        existing_data = {}

    # Cập nhật dữ liệu mới vào secret.json
    existing_data.update(metadata)

    with open(secret_file, 'w') as f:
        json.dump(existing_data, f, indent=4)

    # Bước 5: Hệ thống kết xuất khóa Kprivate cho người dùng thành tệp
    private_key_file = user_name + '_private_key.pem'
    with open(private_key_file, 'wb') as priv_file:
        priv_file.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        ))

    print(f"Tập tin được mã hóa thành công: {encrypted_file}")
    print(f"Thông tin đã được lưu trong: {secret_file}")
    print(f"Khóa riêng tư được lưu tại: {private_key_file}")
