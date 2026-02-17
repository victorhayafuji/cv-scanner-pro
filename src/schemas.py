from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# --- SCHEMAS DE AUTENTICAÇÃO ---

class UserCreate(BaseModel):
    email: str
    password: str
    nome_empresa: str

class UserLogin(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

# --- SCHEMAS DE DADOS (BI/IA) ---

class ResultadoIA(BaseModel):
    """Modelo rigoroso para validação da saída da IA antes de salvar."""
    nome_candidato: str
    cargo_alvo: str
    score_aderencia: int
    nivel_senioridade: str
    principais_skills: str
    gaps_identificados: str
    parecer_resumido: str
    data_analise: datetime
