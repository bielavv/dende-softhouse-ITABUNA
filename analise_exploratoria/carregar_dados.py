
import csv
import sys
import os

# Adiciona a pasta principal ao path

pasta_principal = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(pasta_principal)

from dende_statistics import Statistics

def carregar_dados():

    nome_arquivo = 'spotify_data_clean.csv'
    
    # validação 1.  o arquivo existe?

    if not os.path.exists(nome_arquivo):
        print(f" ERRO: Arquivo '{nome_arquivo}' não encontrado!")
        print(f"   Pasta atual: {os.getcwd()}")
        return None, None
    
    dados = {}
    
    # colunas numéricas pré definidas para conversão

    colunas_numericas = [
        'track_popularity',
        'artist_popularity',
        'artist_followers',
        'album_total_tracks',
        'track_duration_min'
    ]
    
    try:
        with open(nome_arquivo, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            colunas = reader.fieldnames
            
            # inicializa listas
            for coluna in colunas:
                dados[coluna] = []
            
            # carrega dados
            for linha in reader:
                for coluna in colunas:
                    valor = linha[coluna]
                    
                    if coluna in colunas_numericas:
                        # converte para número
                        try:
                            valor_limpo = str(valor).strip().strip('"').strip("'")
                            if valor_limpo == '' or valor_limpo == 'N/A':
                                dados[coluna].append(0)
                            else:
                                dados[coluna].append(float(valor_limpo))
                        except:
                            dados[coluna].append(0)
                    else:
                        # mantém como string
                        dados[coluna].append(str(valor).strip())
        
        print(f"Arquivo carregado: {len(dados[colunas[0]])} músicas")
        
        # cria objeto Statistics
        stats = Statistics(dados)
        print("✅ Dataset validado com sucesso!")
        
        
        return dados, stats
        
    except Exception as e:
        print(f" Erro ao carregar dados: {e}")
        return None, None

# Se executado diretamente, apenas testa o carregamento

if __name__ == "__main__":
    dados, stats = carregar_dados()
    
    if dados and stats:
        print("\n Informações básicas:")
        print(f" Músicas: {len(dados['track_id'])}")
        print(f" Colunas: {len(dados.keys())}")
        print(f" Artistas únicos: {len(stats.itemset('artist_name'))}")