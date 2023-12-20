from cryptography.fernet import Fernet

def generate_key():
    return Fernet.generate_key()

def create_cipher(key):
    return Fernet(key)

def encrypt_credentials(username, password, cipher):
    encrypted_username = cipher.encrypt(username.encode()).decode()
    encrypted_password = cipher.encrypt(password.encode()).decode()
    return encrypted_username, encrypted_password

def decrypt_credentials(encrypted_username, encrypted_password, cipher):
    username = cipher.decrypt(encrypted_username.encode()).decode()
    password = cipher.decrypt(encrypted_password.encode()).decode()
    return username, password

# Credenciais
API_USERNAME = "chicoreis"
API_PASSWORD = "123123"

# Gerar e armazenar chave (deve ser feito uma vez)
KEY = generate_key()
with open('encryption_key.key', 'wb') as key_file:
    key_file.write(KEY)

# Criar instância do Fernet
CIPHER = create_cipher(KEY)

# Armazenar credenciais criptografadas
ENCRYPTED_USERNAME, ENCRYPTED_PASSWORD = encrypt_credentials(API_USERNAME, API_PASSWORD, CIPHER)
