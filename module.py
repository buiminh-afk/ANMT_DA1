import os
import json
import hashlib
import aes
import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes


def encrypt_module(filepath):
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

    print(f"Tập tin được mã hóa thành công: {encrypted_file}")
    print(f"Thông tin đã được lưu trong: {secret_file}")
    print(f"Khóa riêng tư được lưu tại: {private_key_file}")


def decrypt_module(encrypted_file, private_key_file):
    # Bước 1: Người dùng chọn tập tin cần giải mã và khóa riêng tư

    print("HHELLO")
    with open(private_key_file, 'rb') as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
        )

    # Bước 2: Tính hash SHA-1 của khóa riêng tư
    sha1_hash = hashlib.sha1(private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )).hexdigest()

    # Bước 3: Đọc secret.json và kiểm tra SHA-1 hash
    secret_file = 'secret.json'
    if not os.path.exists(secret_file):
        print(f"File {secret_file} không tồn tại.")
        return 0, f"File {secret_file} không tồn tại."

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
        print("Không tìm thấy khóa tương ứng trong secret.json.")
        return 0, "Không tìm thấy khóa tương ứng trong secret.json."

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

    print(f"Tập tin đã được giải mã thành công: {decrypted_file}")
    return 1, decrypted_file


def main():
    decrypt_module(
        'C:\Tài liệu\An ninh mang tinh\ANMT_DA1\\test\\test_encrypt.txt', 'C:\Tài liệu\An ninh mang tinh\ANMT_DA1\\abcd.txt_private_key.pem')


if __name__ == "__main__":
    main()
