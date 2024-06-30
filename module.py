import os
import json
import hashlib
import aes
import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
import customtkinter as ctk


def hash_private_key_sha1(private_key):
    return hashlib.sha1(private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )).hexdigest()


def hash_private_key_sha256(private_key):
    return hashlib.sha256(private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )).hexdigest()


def encrypt_module(filepath, result_label):
    try:
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
        sha1_hash = hash_private_key_sha1(private_key=private_key)

        metadata = {
            file_name: {
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
        private_key_file = file_name + '_private_key.pem'
        with open(private_key_file, 'wb') as priv_file:
            priv_file.write(private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()
            ))

        result_label.configure(text=f"Tập tin được mã hóa thành công: {encrypted_file}\n"
                               f"Thông tin đã được lưu trong: {secret_file}\n"
                               f"Khóa riêng tư được lưu tại: {private_key_file}")
    except Exception as e:
        result_label.configure(text=f"Lỗi: {e}")


def decrypt_module(encrypted_file, private_key_file, result_label):
    try:
        # Bước 1: Người dùng chọn tập tin cần giải mã và khóa riêng tư
        with open(private_key_file, 'rb') as key_file:
            private_key = serialization.load_pem_private_key(
                key_file.read(),
                password=None,
            )

        # Bước 2: Tính hash SHA-1 của khóa riêng tư
        sha1_hash = hash_private_key_sha1(private_key)

        # Bước 3: Đọc secret.json và kiểm tra SHA-1 hash
        secret_file = 'secret.json'
        if not os.path.exists(secret_file):
            result_label.configure(text=f"File {secret_file} không tồn tại.")
            return

        with open(secret_file, 'r') as f:
            secret_data = json.load(f)

        # Tìm SHA-1 trong secret.json
        user_name = None
        encrypted_key_hex = None
        for user, data in secret_data.items():
            if data["SHA-1"] == sha1_hash:
                user_name = user
                encrypted_key_hex = data["Kx"]
                break

        if user_name is None:
            result_label.configure(
                text="Không tìm thấy khóa tương ứng trong secret.json.")
            return

        # Bước 4: Giải mã khóa AES bằng khóa riêng tư
        encrypted_key = bytes.fromhex(encrypted_key_hex)
        aes_key_hex = private_key.decrypt(
            encrypted_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        aes_key = bytes.fromhex(aes_key_hex.decode())

        # Bước 5: Giải mã tập tin bằng khóa AES
        decrypted_file = encrypted_file.replace('_encrypt', '_decrypt')
        aes.decrypt_file_aes(aes_key, encrypted_file, decrypted_file)

        result_label.configure(
            text=f"Tập tin đã được giải mã thành công: {decrypted_file}")
    except Exception as e:
        result_label.configure(text=f"Lỗi: {e}")
