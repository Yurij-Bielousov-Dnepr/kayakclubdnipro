import os
import json
from google.oauth2.credentials import Credentials

def get_google_sheets_credentials():
    # Шлях до файлу конфігурації JSON із ключами API
    config_file_path = os.path.join(os.path.dirname(__file__), 'path/to/your_config.json')

    # Завантажуємо дані з файлу конфігурації
    with open(config_file_path) as f:
        config_data = json.load(f)

    # Перевіряємо, чи всі необхідні ключі є в конфігурації
    required_keys = ['type', 'project_id', 'private_key_id', 'private_key', 'client_email', 'client_id', 'auth_uri', 'token_uri', 'auth_provider_x509_cert_url', 'client_x509_cert_url']
    for key in required_keys:
        if key not in config_data:
            raise ValueError(f"Missing required key in the config file: {key}")

    # Створюємо об'єкт Credentials для авторизації Google Sheets API
    credentials = Credentials.from_authorized_user_info(config_data)

    return credentials