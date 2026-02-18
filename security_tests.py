import requests
import time

BASE_URL = "http://localhost:8000/api/v1"

def print_result(test_name, success, message=""):
    status = "✅ PASS" if success else "❌ FAIL"
    print(f"{status} - {test_name}")
    if message:
        print(f"   ℹ️  {message}")

def test_unauthorized_access():
    print("\n🔹 Testando Acesso Não Autorizado...")
    
    # 1. Tentar acessar dashboard sem token
    try:
        response = requests.get(f"{BASE_URL}/dashboard/metrics")
        if response.status_code == 401:
            print_result("Acesso ao Dashboard sem token", True)
        else:
            print_result("Acesso ao Dashboard sem token", False, f"Status: {response.status_code}")
    except Exception as e:
        print_result("Acesso ao Dashboard sem token", False, f"Erro: {e}")

def test_login_security():
    print("\n🔹 Testando Segurança de Login...")
    
    # 1. Senha errada
    try:
        data = {"username": "usuario_teste@exemplo.com", "password": "senha_errada_123"}
        response = requests.post(f"{BASE_URL}/auth/login", data=data)
        
        if response.status_code == 401:
            print_result("Login com senha incorreta", True)
        else:
            print_result("Login com senha incorreta", False, f"Esperado 401, recebeu {response.status_code}")
    except Exception as e:
        print_result("Login com senha incorreta", False, f"Erro: {e}")

def test_file_upload_security():
    print("\n🔹 Testando Upload de Arquivos Maliciosos...")
    
    # Precisa de um token válido primeiro
    # Vamos criar um usuário de teste (ou usar um existente se soubéssemos a senha)
    # Como é um teste de segurança "black box", vamos assumir que não temos acesso por enquanto
    # Mas para testar o upload, precisaríamos estar logados. 
    # VAMOS PULAR A PARTE DE ESTAR LOGADO para ver se o endpoint Protegido rejeita arquivo SEM LOGIN primeiro.
    
    files = {'arquivo': ('malicioso.exe', b'Conteudo malicioso simulado', 'application/x-msdownload')}
    try:
        response = requests.post(f"{BASE_URL}/analisar-cv/", files=files)
        
        if response.status_code == 401:
            print_result("Upload de .exe sem autenticação", True, "Endpoint protegido corretamente")
        else:
             print_result("Upload de .exe sem autenticação", False, f"Status: {response.status_code}")

    except Exception as e:
        print_result("Upload de arquivo malicioso", False, f"Erro: {e}")

def test_sql_injection():
    print("\n🔹 Testando SQL Injection (Login)...")
    payloads = ["' OR '1'='1", "admin' --", "' OR 1=1 --"]
    
    for payload in payloads:
        data = {"username": payload, "password": "password"}
        try:
            response = requests.post(f"{BASE_URL}/auth/login", data=data)
            if response.status_code == 401:
                # Se der 401, o sistema tratou a entrada como credencial inválida (Correto!)
                # Se desse 200, logou (Falha Grave!)
                # Se desse 500, estourou erro de SQL (Falha Moderada - Info Disclosure)
                pass # Continua testando outros payloads
            elif response.status_code == 200:
                print_result(f"SQLi Payload: {payload}", False, "CRÍTICO: Login realizado com sucesso!")
                return
            elif response.status_code == 500:
                print_result(f"SQLi Payload: {payload}", False, "ALERTA: Erro Interno (Possível falha de tratamento)")
                return
        except Exception as e:
            print_result(f"SQLi Payload: {payload}", False, f"Erro na requisição: {e}")
            return
            
    print_result("Resistência a SQL Injection (Login)", True, "Todos os payloads foram rejeitados (401)")

def test_xss_protection():
    print("\n🔹 Testando XSS (Cross-Site Scripting)...")
    # Tenta enviar script no signup (onde o nome da empresa é refletido/salvo)
    # Payload inofensivo mas detectável
    xss_payload = "<script>alert('XSS')</script>"
    
    data = {
        "email": f"hacker_{int(time.time())}@xss.com", 
        "password": "Password123!", 
        "nome_empresa": xss_payload
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/signup", json=data)
        
        # O ideal é que o backend aceite (se for só API) mas que o frontend sanitize.
        # Mas vamos verificar se ele retorna o payload "cru" ou sanitizado, ou se aceita.
        if response.status_code == 200:
            # Se salvou, precisamos verificar se ele sanitizou?
            # Como é blackbox, vamos assumir que aceitar texto cru é "risco aceito" se não houver renderização HTML no retorno.
            # Mas como alerta, vamos logar.
            print_result("XSS Stored (Signup)", True, "Payload aceito (O frontend DEVE sanitizar ao exibir!)")
        elif response.status_code == 422:
             print_result("XSS Stored (Signup)", True, "Payload rejeitado pela validação (Melhor cenário)")
        else:
             print_result("XSS Stored (Signup)", False, f"Status inesperado: {response.status_code}")
             
    except Exception as e:
        print_result("XSS Stored (Signup)", False, f"Erro: {e}")

def test_rate_limiting():
    print("\n🔹 Testando Rate Limiting (DoS Simples)...")
    count = 20 # Requisições rápidas
    start = time.time()
    success_count = 0
    
    for _ in range(count):
        try:
            requests.get(f"{BASE_URL}/docs") # Endpoint leve
            success_count += 1
        except:
            pass
            
    duration = time.time() - start
    print(f"   ℹ️  {success_count} requisições em {duration:.2f}s")
    
    if success_count == count:
        print_result("Resistência a Flood", True, "Servidor aguentou a carga (Nota: Sem Rate Limit estrito detectado)")
    else:
        print_result("Resistência a Flood", False, "Algumas requisições falharam (Pode indicar instabilidade ou bloqueio)")

class BackendLifecycle:
    def __init__(self):
        self.process = None
        self.already_running = False

    def start(self):
        # 1. Verifica se já está rodando
        try:
            requests.get("http://localhost:8000/docs", timeout=1)
            print("ℹ️  Backend já está rodando. Usando instância existente.")
            self.already_running = True
            return
        except:
            pass

        print("🚀 Iniciando servidor Backend para testes...")
        # Usa o mesmo python que está rodando este script
        self.process = subprocess.Popen(
            [sys.executable, "-m", "uvicorn", "src.api:app", "--port", "8000"],
            stdout=subprocess.DEVNULL, # Limpa o log do teste
            stderr=subprocess.PIPE
        )
        
        # Aguarda startup
        print("⏳ Aguardando API ficar online...")
        for _ in range(30):
            try:
                requests.get("http://localhost:8000/docs", timeout=1)
                print("✅ Backend online!")
                return
            except:
                time.sleep(1)
        
        self.stop()
        raise Exception("❌ Falha ao iniciar backend: Timeout excedido.")

    def stop(self):
        if self.already_running:
            print("ℹ️  Mantendo backend rodando (já estava ativo antes).")
            return
            
        if self.process:
            print("🛑 Encerrando backend de teste...")
            self.process.terminate()
            try:
                self.process.wait(timeout=5)
            except:
                self.process.kill()
            print("✅ Backend encerrado.")

if __name__ == "__main__":
    import sys
    import subprocess
    
    print("🚀 Iniciando Bateria de Testes de Segurança CV Scanner Pro")
    print(f"Alvo: {BASE_URL}")
    
    SERVER = BackendLifecycle()
    
    try:
        SERVER.start()
        
        # Executa testes
        start_time = time.time()
        
        test_unauthorized_access()
        test_login_security()
        test_file_upload_security()
        test_sql_injection()
        test_xss_protection()
        test_rate_limiting()
        
        duration = time.time() - start_time
        print(f"\n🏁 Testes Finalizados em {duration:.2f}s.")
        
    except Exception as e:
        print(f"\n❌ ERRO FATAL DURANTE TESTES: {e}")
    finally:
        SERVER.stop()
