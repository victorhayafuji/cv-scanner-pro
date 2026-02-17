import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import requests
import json
from src.services.auth_handler import create_access_token, criar_usuario, buscar_usuario_por_email

BASE_URL = "http://127.0.0.1:8000/api/v1"
TEST_EMAIL = "security_tester@example.com"
TEST_PASS = "sec123"

def run_test(name, func):
    print(f"--- Testando: {name} ---")
    try:
        func()
        print("✅ PASSOU")
    except Exception as e:
        print(f"❌ FALHOU: {e}")
        # sys.exit(1) # Não para o script, roda todos

def setup_user():
    if not buscar_usuario_por_email(TEST_EMAIL):
        criar_usuario(TEST_EMAIL, TEST_PASS, "Security Corp")

def test_login_failure():
    resp = requests.post(f"{BASE_URL}/auth/login", data={"username": TEST_EMAIL, "password": "wrong_password"})
    if resp.status_code != 401:
        raise Exception(f"Esperado 401, recebeu {resp.status_code}")

def test_protected_route_no_token():
    resp = requests.get(f"{BASE_URL}/dashboard/metrics")
    if resp.status_code != 401:
        raise Exception(f"Esperado 401, recebeu {resp.status_code}")

def test_protected_route_bad_token():
    headers = {"Authorization": "Bearer tokeninválido123"}
    resp = requests.get(f"{BASE_URL}/dashboard/metrics", headers=headers)
    if resp.status_code != 401:
        raise Exception(f"Esperado 401, recebeu {resp.status_code}")

def test_data_leakage():
    # Login correto para pegar token
    resp = requests.post(f"{BASE_URL}/auth/login", data={"username": TEST_EMAIL, "password": TEST_PASS})
    token = resp.json()["access_token"]
    
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.get(f"{BASE_URL}/auth/me", headers=headers)
    data = resp.json()
    
    if "senha_hash" in data or "password" in data:
        raise Exception("VAZAMENTO DE DADOS: Senha ou Hash retornados na API!")

def test_invalid_upload():
    # Login correto
    resp = requests.post(f"{BASE_URL}/auth/login", data={"username": TEST_EMAIL, "password": TEST_PASS})
    token = resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # Cria arquivo fake .txt
    files = {'arquivo': ('teste.txt', 'conteudo texto plano', 'text/plain')}
    resp = requests.post(f"{BASE_URL}/analisar-cv/", files=files, headers=headers)
    
    # Esperado: 400 ou 500 (dependendo da validação do pdf_handler)
    # O pdf_handler retorna None se não for PDF ou imagem, e a API levanta 400
    if resp.status_code != 400:
         raise Exception(f"Esperado 400 para arquivo inválido, recebeu {resp.status_code}. Detalhe: {resp.text}")

if __name__ == "__main__":
    setup_user()
    run_test("Login com Senha Errada", test_login_failure)
    run_test("Acesso sem Token", test_protected_route_no_token)
    run_test("Acesso com Token Inválido", test_protected_route_bad_token)
    run_test("Vazamento de Senha na API", test_data_leakage)
    run_test("Upload de Arquivo Inválido (.txt)", test_invalid_upload)
