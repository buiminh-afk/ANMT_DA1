import os
import json
import hashlib
import aes
import rsa
from cryptography.hazmat.primitives import serialization

folder = './test/'


def main():
    # Bước 1: Người dùng nhập tên tập tin cần mã hóa và tên người dùng
    input_file = input("Nhập tên tập tin cần mã hóa: ")
    user_name = input("Nhập tên người dùng để đặt tên cho private key: ")

    # Bước 2: Hệ thống phát sinh khóa bí mật Ks và mã hóa tập tin P thành tập tin C bằng AES
    aes_key = aes.generate_aes_key()
    encrypted_file = input_file + '_encrypt'
    aes.encrypt_file_aes(aes_key, input_file, encrypted_file)

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
    with open(folder + private_key_file, 'wb') as priv_file:
        priv_file.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        ))

    print(f"Tập tin được mã hóa thành công: {encrypted_file}")
    print(f"Thông tin đã được lưu trong: {secret_file}")
    print(f"Khóa riêng tư được lưu tại: {private_key_file}")


if __name__ == "__main__":
    main()
