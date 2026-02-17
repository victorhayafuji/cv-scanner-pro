import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import requests
import json
from src.services.auth_handler import create_access_token, criar_usuario, buscar_usuario_por_email

# Config
BASE_URL = "http://127.0.0.1:8000/api/v1"
TEST_EMAIL = "analytics_tester@example.com"

def test_analytics_endpoint():
    print("=== Testando Endpoint de Analytics ===")
    
    # 1. Garantir que usuário existe
    if not buscar_usuario_por_email(TEST_EMAIL):
        criar_usuario(TEST_EMAIL, "pass123", "Tester Corp")
        print(f"✅ Usuário {TEST_EMAIL} criado.")
    
    # 2. Gerar Token 
    token = create_access_token(data={"sub": TEST_EMAIL})
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(f"{BASE_URL}/dashboard/metrics", headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Requisição Sucesso (200 OK)")
            
            if "all_records" in data:
                count = len(data["all_records"])
                print(f"✅ Campo 'all_records' encontrado com {count} registros.")
                if count > 0:
                    print(f"   Exemplo de registro: {data['all_records'][0].keys()}")
            else:
                print("❌ ERRO: Campo 'all_records' ausente na resposta.")
        else:
            print(f"❌ Falha na requisição: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"❌ Erro de conexão: {e}")

if __name__ == "__main__":
    test_analytics_endpoint()
