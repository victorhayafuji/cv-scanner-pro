from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
import bcrypt  # Usando bcrypt diretamente
import pandas as pd
import os
import uuid
from src.config import Config

# --- CONFIGURAÇÕES ---
# Em produção, mova para variáveis de ambiente
SECRET_KEY = "sua_secret_key_super_secreta_trocar_em_prod" 
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 300 # 5 horas para facilitar testes
DB_USUARIOS = "usuarios.xlsx"

# --- FUNÇÕES DE BANCO DE DADOS (EXCEL) ---

def carregar_usuarios():
    """Carrega o DataFrame de usuários ou cria um novo se não existir."""
    if not os.path.exists(DB_USUARIOS):
        df = pd.DataFrame(columns=['id_usuario', 'email', 'senha_hash', 'nome_empresa', 'data_criacao'])
        df.to_excel(DB_USUARIOS, index=False)
        return df
    return pd.read_excel(DB_USUARIOS)

def salvar_usuario_excel(novo_usuario_dict):
    """Salva um novo usuário no Excel com tratamento de concorrência básico."""
    try:
        df = carregar_usuarios()
        
        # Verifica se email já existe
        if not df[df['email'] == novo_usuario_dict['email']].empty:
            raise ValueError("Email já cadastrado.")

        novo_df = pd.DataFrame([novo_usuario_dict])
        df_final = pd.concat([df, novo_df], ignore_index=True)
        df_final.to_excel(DB_USUARIOS, index=False)
    except PermissionError:
        raise Exception("Erro de Permissão: Feche o arquivo usuarios.xlsx e tente novamente.")

def buscar_usuario_por_email(email: str):
    """Retorna o dicionário do usuário ou None."""
    df = carregar_usuarios()
    usuario = df[df['email'] == email]
    if usuario.empty:
        return None
    return usuario.iloc[0].to_dict()

# --- FUNÇÕES DE SEGURANÇA ---

def verify_password(plain_password, hashed_password):
    # Converte strings para bytes
    if isinstance(plain_password, str):
        plain_password = plain_password.encode('utf-8')
    if isinstance(hashed_password, str):
        hashed_password = hashed_password.encode('utf-8')
    return bcrypt.checkpw(plain_password, hashed_password)

def get_password_hash(password):
    if isinstance(password, str):
        password = password.encode('utf-8')
    # Gera o hash e retorna como string para salvar no JSON/Excel
    return bcrypt.hashpw(password, bcrypt.gensalt()).decode('utf-8')

def criar_usuario(email, senha_raw, empresa):
    """Cria novo usuário com hash de senha."""
    senha_hash = get_password_hash(senha_raw)
    novo_usuario = {
        'id_usuario': str(uuid.uuid4()),
        'email': email,
        'senha_hash': senha_hash,
        'nome_empresa': empresa,
        'data_criacao': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    salvar_usuario_excel(novo_usuario)
    return novo_usuario

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
