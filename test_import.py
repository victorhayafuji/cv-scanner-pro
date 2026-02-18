"""
Script de teste para verificar importações das bibliotecas de IA do Google.
"""

try:
    from langchain_google_genai import ChatGoogleGenerativeAI
    print(f"Success import from langchain_google_genai: {ChatGoogleGenerativeAI}")
except ImportError:
    print("Failed import from langchain_google_genai")

# langchain_community imports removed as they are deprecated and were causing errors.
# We are using langchain_google_genai instead.

import google.generativeai as genai
print(f"google.generativeai version: {genai.__version__}")
