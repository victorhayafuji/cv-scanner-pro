import os

# Configurações
SOURCE_DIRS = [
    "src",
    "frontend/src",
    "scripts",
    ".",  # Raiz (para main.py, etc)
]

# Extensões para incluir
INCLUDE_EXTENSIONS = {
    ".py", ".js", ".jsx", ".css", ".html", ".md", ".json", ".sql"
}

# Pastas para ignorar
IGNORE_DIRS = {
    "node_modules", ".venv", "__pycache__", ".git", ".idea", "dist", "build", "txt-files", "coverage", "brain", ".gemini"
}

# Arquivos específicos para ignorar
IGNORE_FILES = {
    "package-lock.json", "dicionario_competencias.json", "dados_bi.xlsx", "dados_bi_mock.xlsx", "project_bundle.txt"
}

OUTPUT_FILE = "project_bundle.txt"

def should_process(file_path):
    # Verifica extensão
    _, ext = os.path.splitext(file_path)
    if ext not in INCLUDE_EXTENSIONS:
        return False
    
    filename = os.path.basename(file_path)
    if filename in IGNORE_FILES:
        return False
        
    return True

def sync_files():
    base_path = os.getcwd()
    output_path = os.path.join(base_path, OUTPUT_FILE)
    
    count = 0
    
    with open(output_path, "w", encoding="utf-8") as f_out:
        f_out.write(f"# PROJECT CODEBASE BUNDLE\n")
        f_out.write(f"# Contém todo o código fonte do projeto concatenado.\n\n")

        # Set para rastrear arquivos já processados e evitar duplicidade
        processed_files = set()

        for relative_start_dir in SOURCE_DIRS:
            start_path = os.path.join(base_path, relative_start_dir)
            
            if not os.path.exists(start_path):
                print(f"Aviso: Diretório fonte '{start_path}' não encontrado.")
                continue
                
            print(f"Processando diretório: {relative_start_dir}")

            for root, dirs, files in os.walk(start_path):
                # Filtra diretórios ignorados in-place
                dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
                
                for file in files:
                    file_path = os.path.join(root, file)
                    
                    if should_process(file_path):
                        # Caminho relativo para o header/identificação
                        rel_path = os.path.relpath(file_path, base_path)
                        
                        # Evita processar o próprio bundle
                        if rel_path == OUTPUT_FILE:
                            continue
                        
                        # Evita duplicidade (ex: '.' inclui 'src', então 'src/api.py' apareceria 2x)
                        if rel_path in processed_files:
                            continue

                        try:
                            with open(file_path, "r", encoding="utf-8") as f_in:
                                content = f_in.read()
                                
                            f_out.write(f"\n{'='*50}\n")
                            f_out.write(f"FILE: {rel_path}\n")
                            f_out.write(f"{'='*50}\n\n")
                            f_out.write(content)
                            f_out.write("\n")
                            
                            print(f"Adicionado: {rel_path}")
                            processed_files.add(rel_path)
                            count += 1
                            
                        except Exception as e:
                            print(f"Erro ao processar {file}: {e}")
                            
    print(f"\nConcluído! {count} arquivos unificados em '{OUTPUT_FILE}'.")

if __name__ == "__main__":
    sync_files()
