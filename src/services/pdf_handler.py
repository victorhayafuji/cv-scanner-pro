import os
import tempfile
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.config import Config


def processar_pdf(uploaded_file):
    """Salva temporariamente, lê e fatia o PDF."""
    print(f"Iniciando processamento de PDF...")
    try:
        # 1. Salvar arquivo temporário (Windows friendly)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            conteudo = uploaded_file.read()
            print(f"Salvo arquivo temporário: {tmp.name}, Tamanho: {len(conteudo)} bytes")
            if len(conteudo) == 0:
                print("ERRO: Arquivo recebido está vazio (0 bytes).")
                return None
            tmp.write(conteudo)
            tmp_path = tmp.name

        # 2. Carregar
        print(f"Tentando carregar PDF com PyPDFLoader: {tmp_path}")
        loader = PyPDFLoader(tmp_path)
        docs = loader.load()
        print(f"PDF carregado com sucesso. Páginas: {len(docs)}")

        # 3. Limpeza
        try:
            os.remove(tmp_path)
        except Exception as e:
            print(f"Aviso: Não foi possível remover arquivo temporário {tmp_path}: {e}")

        # 4. Validação de Conteúdo (Texto Vazio/Imagem)
        tem_texto = any(d.page_content.strip() for d in docs)
        if not tem_texto:
             print("AVISO: Nenhuma texto extraído. PDF pode ser imagem digitalizada.")
             return None

        # 5. Fatiamento (Chunking)
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=Config.CHUNK_SIZE,
            chunk_overlap=Config.CHUNK_OVERLAP
        )
        return splitter.split_documents(docs)

    except Exception as e:
        import traceback
        print(f"ERRO CRÍTICO no PDF Handler: {e}")
        traceback.print_exc()
        return None