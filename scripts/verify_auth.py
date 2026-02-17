import requests
import uuid

BASE_URL = "http://127.0.0.1:8000/api/v1"

def test_auth_flow():
    # 1. Signup
    email = f"test_{uuid.uuid4()}@example.com"
    password = "securepassword123"
    empresa = "Tech Corp"
    
    print(f"Tentando criar usuário: {email}")
    response = requests.post(f"{BASE_URL}/auth/signup", json={
        "email": email,
        "password": password,
        "nome_empresa": empresa
    })
    
    if response.status_code == 200:
        print("✅ Signup com sucesso!")
    else:
        print(f"❌ Falha no Signup: {response.text}")
        return

    # 2. Login
    print("Tentando login...")
    response = requests.post(f"{BASE_URL}/auth/login", data={
        "username": email,
        "password": password
    })
    
    if response.status_code == 200:
        token = response.json().get("access_token")
        print("✅ Login com sucesso! Token recebido.")
    else:
        print(f"❌ Falha no Login: {response.text}")
        return

    # 3. Access Protected Route (Dashboard Metrics)
    print("Tentando acessar rota protegida (/dashboard/metrics)...")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/dashboard/metrics", headers=headers)
    
    if response.status_code == 200:
        print(f"✅ Acesso autorizado! Metrícas: {response.json()}")
    else:
        print(f"❌ Falha no acesso protegido: {response.text}")

if __name__ == "__main__":
    try:
        test_auth_flow()
    except Exception as e:
        print(f"Erro na verificação: {e}")
        print("Verifique se o servidor está rodando!")
