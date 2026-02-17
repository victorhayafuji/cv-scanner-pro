import sys
import os

# Adiciona a pasta raiz ao path do Python para encontrar os módulos 'src'
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from streamlit.web import cli as stcli

if __name__ == "__main__":
    # Truque para rodar o streamlit via python main.py
    sys.argv = ["streamlit", "run", "src/ui/dashboard.py"]
    sys.exit(stcli.main())