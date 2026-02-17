import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import requests
from src.services.auth_handler import create_access_token, criar_usuario, buscar_usuario_por_email

BASE_URL = "http://127.0.0.1:8000/api/v1"
TEST_EMAIL = "me_tester@example.com"

def test_auth_me():
    print("=== Testando Endpoint /auth/me ===")
    
    # 1. Garantir usuário
    if not buscar_usuario_por_email(TEST_EMAIL):
        criar_usuario(TEST_EMAIL, "pass123", "Me Corp")
        print(f"Usuário {TEST_EMAIL} criado.")
    
    # 2. Gerar Token
    token = create_access_token(data={"sub": TEST_EMAIL})
    
    # 3. Request /auth/me
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.get(f"{BASE_URL}/auth/me", headers=headers)
        if response.status_code == 200:
            data = response.json()
            print("✅ Sucesso!")
            print(f"Email: {data.get('email')}")
            print(f"Empresa: {data.get('empresa')}")
            
            if data.get('email') == TEST_EMAIL:
                print("✅ Email corresponde.")
                sys.exit(0)
            else:
                print("❌ Email incorreto.")
                sys.exit(1)
        else:
            print(f"❌ Erro: {response.status_code} - {response.text}")
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ Exceção: {e}")
        sys.exit(1)

if __name__ == "__main__":
    test_auth_me()
