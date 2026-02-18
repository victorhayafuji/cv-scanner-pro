try:
    from langchain_google_genai import ChatGoogleGenerativeAI
    print("Success import from langchain_google_genai")
except ImportError:
    print("Failed import from langchain_google_genai")

try:
    from langchain_community.chat_models import ChatGoogleGenerativeAI
    print("Success import from langchain_community.chat_models")
except ImportError:
    print("Failed import from langchain_community.chat_models")

import google.generativeai as genai
print(f"google.generativeai version: {genai.__version__}")
