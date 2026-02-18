import subprocess
import sys
import os
import signal
import time
import socket

def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

def run_services():
    print("🚀 Iniciando CV Engine Pro (Full Stack)...")
    
    processes = []

    # 1. Backend (FastAPI) - Port 8000
    if is_port_in_use(8000):
        print("⚠️  Porta 8000 já está em uso. Pulando inicialização do Backend.")
    else:
        print("🔹 Iniciando Backend (Porta 8000)...")
        
        # Tenta encontrar o python do .venv primeiro
        venv_python = os.path.join(os.getcwd(), ".venv", "Scripts", "python.exe")
        if os.path.exists(venv_python):
            python_exec = venv_python
        else:
            python_exec = sys.executable

        backend = subprocess.Popen(
            [python_exec, "-m", "uvicorn", "src.api:app", "--reload", "--port", "8000"],
            cwd=os.getcwd()
        )
        processes.append(backend)
    
    # 2. Frontend (Vite/React) - Port 5173
    # Vite default port is 5173, but it might auto-switch if busy. 
    # We'll check 5173 just to be safe/consistent with the log message.
    if is_port_in_use(5173):
        print("⚠️  Porta 5173 já está em uso. Pulando inicialização do Frontend.")
    else:
        print("🔹 Iniciando Frontend (Porta 5173)...")
        frontend_dir = os.path.join(os.getcwd(), "frontend")
        # npm.cmd para Windows, npm para Linux/Mac
        npm_cmd = "npm.cmd" if os.name == "nt" else "npm"
        
        frontend = subprocess.Popen(
            [npm_cmd, "run", "dev"],
            cwd=frontend_dir,
            shell=True
        )
        processes.append(frontend)

    if not processes:
        print("✅ Todos os serviços já parecem estar rodando externamente.")
        # Mantém o script rodando para não fechar imediatamente se o usuário quiser
        # mas como não gerenciamos nada, talvez fosse melhor sair?
        # Vamos manter rodando para ele servir como um "painel" dummy se quiser.
        print("ℹ️  Pressione Ctrl+C para encerrar este monitor (não fechará serviços externos).")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Encerrando serviços iniciados por este script...")
        for p in processes:
            try:
                p.terminate()
            except:
                pass
        sys.exit(0)

if __name__ == "__main__":
    run_services()