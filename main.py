import subprocess
import sys
import os
import signal
import time

def run_services():
    print("🚀 Iniciando CV Engine Pro (Full Stack)...")
    
    # 1. Backend (FastAPI)
    print("🔹 Iniciando Backend (Porta 8000)...")
    backend = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "src.api:app", "--reload", "--port", "8000"],
        cwd=os.getcwd()
    )

    # 2. Frontend (Vite/React)
    print("🔹 Iniciando Frontend (Porta 5173)...")
    frontend_dir = os.path.join(os.getcwd(), "frontend")
    # npm.cmd para Windows, npm para Linux/Mac
    npm_cmd = "npm.cmd" if os.name == "nt" else "npm"
    
    frontend = subprocess.Popen(
        [npm_cmd, "run", "dev"],
        cwd=frontend_dir,
        shell=True
    )

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Encerrando serviços...")
        backend.terminate()
        # Para matar o processo node gerado pelo npm run dev no Windows pode ser chato, 
        # mas terminate() no objeto Popen ajuda.
        frontend.terminate()
        sys.exit(0)

if __name__ == "__main__":
    run_services()