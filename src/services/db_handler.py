import pandas as pd
import os
from datetime import datetime

def salvar_candidato_excel(dados: dict, caminho_arquivo="dados_bi.xlsx") -> tuple[bool, str]:
    """
    Salva os dados do candidato em um arquivo Excel (append mode).
    Retorna (Sucesso: bool, Mensagem: str)
    """
    # Adiciona timestamp da execução
    dados["data_analise"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Cria DataFrame com uma única linha
    df_novo = pd.DataFrame([dados])

    try:
        if os.path.exists(caminho_arquivo):
            # Tenta ler o arquivo existente
            try:
                df_antigo = pd.read_excel(caminho_arquivo, engine='openpyxl')
                df_final = pd.concat([df_antigo, df_novo], ignore_index=True)
            except Exception as e:
                return False, f"Erro ao ler arquivo existente: {str(e)}"
        else:
            df_final = df_novo

        # Salva no arquivo (sobrescrevendo com os dados concatenados)
        try:
            df_final.to_excel(caminho_arquivo, index=False, engine='openpyxl')
            return True, "Dados salvos com sucesso!"
        except PermissionError:
            return False, "Erro: O arquivo Excel está aberto. Feche-o e tente novamente."
        except Exception as e:
            return False, f"Erro ao salvar Excel: {str(e)}"

    except Exception as e:
        return False, f"Erro inesperado no DB Handler: {str(e)}"
