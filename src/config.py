# Arquivo: src/config.py

import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

    # SOLUÇÃO: Adicione o sufixo "-latest"
    MODEL_NAME = os.getenv("MODEL_NAME", "gemini-2.5-flash")

    EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
    CHUNK_SIZE = 800
    CHUNK_OVERLAP = 150

    @staticmethod
    def validar():
        if not Config.GOOGLE_API_KEY:
            raise ValueError("A chave GOOGLE_API_KEY não foi encontrada no .env")