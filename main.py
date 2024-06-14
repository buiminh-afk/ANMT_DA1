import aes
import rsa


def main():
    # AES example usage
    aes_key = aes.generate_aes_key()
    aes.encrypt_file_aes(aes_key, 'input.txt', 'encrypted_aes.bin')
    aes.decrypt_file_aes(aes_key, 'encrypted_aes.bin', 'decrypted_aes.txt')

    # RSA example usage
    private_key, public_key = rsa.generate_rsa_key_pair()
    encrypted_text = rsa.encrypt_string_rsa(public_key, 'Hello, RSA!')
    print(f'Encrypted text: {encrypted_text}')
    decrypted_text = rsa.decrypt_string_rsa(private_key, encrypted_text)
    print(f'Decrypted text: {decrypted_text}')


if __name__ == "__main__":
    main()
