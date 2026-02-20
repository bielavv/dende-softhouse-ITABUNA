import sys
import os

# Adiciona a pasta principal ao path

pasta_principal = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(pasta_principal)

# Importa a função de carregar dados

from analise_exploratoria.carregar_dados import carregar_dados

def analisar_explicit(stats, dados):

    print("\n" + "=" * 60)
    print(" ANÁLISE DE CONTEÚDO EXPLÍCITO")
    print("=" * 60)
    
    coluna = 'explicit'
    total_musicas = len(dados[coluna])
    
    # 1. FREQUÊNCIA ABSOLUTA
    print("\nDISTRIBUIÇÃO GERAL:")
    print("-" * 40)
    
    freq_abs = stats.absolute_frequency(coluna)
    explicitas = freq_abs.get('TRUE', 0)
    nao_explicitas = freq_abs.get('FALSE', 0)
    
    print(f"Músicas explícitas (TRUE):    {explicitas:5d} ({explicitas/total_musicas*100:5.1f}%)")
    print(f"Músicas não explícitas (FALSE): {nao_explicitas:5d} ({nao_explicitas/total_musicas*100:5.1f}%)")
    
    # Barrinha visual

    barra_exp = '█' * int((explicitas/total_musicas) * 50)
    barra_nao = '█' * int((nao_explicitas/total_musicas) * 50)
    print(f"\nExplícitas:   {barra_exp} ({explicitas/total_musicas*100:.1f}%)")
    print(f"Não explícitas: {barra_nao} ({nao_explicitas/total_musicas*100:.1f}%)")
    
    # 2. FREQUÊNCIA RELATIVA

    print("\n PROPORÇÃO:")
    print("-" * 40)
    
    freq_rel = stats.relative_frequency(coluna)
    print(f"Proporção de músicas explícitas: {freq_rel.get('TRUE', 0)*100:.1f}%")
    print(f"Proporção de músicas não explícitas: {freq_rel.get('FALSE', 0)*100:.1f}%")
    
    # 3. ANÁLISE DE POPULARIDADE

    print("\n COMPARAÇÃO DE POPULARIDADE:")
    print("-" * 40)
    
    # Separa as popularidades

    pop_explicit = []
    pop_nao_explicit = []
    
    for i, val in enumerate(dados[coluna]):
        pop = dados['track_popularity'][i]
        if val == 'TRUE':
            pop_explicit.append(pop)
        else:
            pop_nao_explicit.append(pop)
    
    # Calcula estatísticas

    if pop_explicit:
        media_exp = sum(pop_explicit) / len(pop_explicit)
        mediana_exp = sorted(pop_explicit)[len(pop_explicit)//2] if pop_explicit else 0
        max_exp = max(pop_explicit) if pop_explicit else 0
        min_exp = min(pop_explicit) if pop_explicit else 0
    else:
        media_exp = mediana_exp = max_exp = min_exp = 0
    
    if pop_nao_explicit:
        media_nao = sum(pop_nao_explicit) / len(pop_nao_explicit)
        mediana_nao = sorted(pop_nao_explicit)[len(pop_nao_explicit)//2] if pop_nao_explicit else 0
        max_nao = max(pop_nao_explicit) if pop_nao_explicit else 0
        min_nao = min(pop_nao_explicit) if pop_nao_explicit else 0
    else:
        media_nao = mediana_nao = max_nao = min_nao = 0
    
    print(f"{'':20} {'Explícitas':15} {'Não explícitas':15} {'Diferença':10}")
    print("-" * 60)
    print(f"Média:          {media_exp:15.1f} {media_nao:15.1f} {media_exp - media_nao:+10.1f}")
    print(f"Mediana:        {mediana_exp:15.1f} {mediana_nao:15.1f} {mediana_exp - mediana_nao:+10.1f}")
    print(f"Máxima:         {max_exp:15.0f} {max_nao:15.0f} {max_exp - max_nao:+10.0f}")
    print(f"Mínima:         {min_exp:15.0f} {min_nao:15.0f} {min_exp - min_nao:+10.0f}")
    
    # 4. DISTRIBUIÇÃO DE POPULARIDADE POR CATEGORIA

    print("\n DISTRIBUIÇÃO DE POPULARIDADE:")
    print("-" * 60)
    
    # Faixas de popularidade

    faixas = [0, 20, 40, 60, 80, 100]
    exp_faixas = [0] * (len(faixas) - 1)
    nao_faixas = [0] * (len(faixas) - 1)
    
    for pop in pop_explicit:
        for i in range(len(faixas)-1):
            if faixas[i] <= pop < faixas[i+1]:
                exp_faixas[i] += 1
                break
        if pop == 100:
            exp_faixas[-1] += 1
    
    for pop in pop_nao_explicit:
        for i in range(len(faixas)-1):
            if faixas[i] <= pop < faixas[i+1]:
                nao_faixas[i] += 1
                break
        if pop == 100:
            nao_faixas[-1] += 1
    
    print(f"{'Faixa':15} {'Explícitas':15} {'Não explícitas':15}")
    print("-" * 45)
    for i in range(len(faixas)-1):
        faixa = f"{faixas[i]}-{faixas[i+1]}"
        perc_exp = (exp_faixas[i] / len(pop_explicit) * 100) if pop_explicit else 0
        perc_nao = (nao_faixas[i] / len(pop_nao_explicit) * 100) if pop_nao_explicit else 0
        print(f"{faixa:15} {exp_faixas[i]:6d} ({perc_exp:5.1f}%)  {nao_faixas[i]:6d} ({perc_nao:5.1f}%)")
    
    # 5. TOP MÚSICAS EXPLÍCITAS

    print("\n TOP 10 MÚSICAS EXPLÍCITAS MAIS POPULARES:")
    print("-" * 60)
    print(f"{'#':3} {'Música':45} {'Artista':25} {'Pop':5}")
    print("-" * 60)
    
    # Filtra apenas explícitas e ordena por popularidade

    explicit_indices = [i for i, val in enumerate(dados[coluna]) if val == 'TRUE']
    explicit_ordenados = sorted(explicit_indices, 
                               key=lambda i: dados['track_popularity'][i], 
                               reverse=True)[:10]
    
    for i, idx in enumerate(explicit_ordenados, 1):
        nome = dados['track_name'][idx][:42]
        artista = dados['artist_name'][idx][:23]
        pop = dados['track_popularity'][idx]
        print(f"{i:3} {nome:45} {artista:25} {pop:5.0f}")
    
    # 6. TOP MÚSICAS NÃO EXPLÍCITAS

    print("\n🏆 TOP 10 MÚSICAS NÃO EXPLÍCITAS MAIS POPULARES:")
    print("-" * 60)
    print(f"{'#':3} {'Música':45} {'Artista':25} {'Pop':5}")
    print("-" * 60)
    
    # Filtra apenas não explícitas e ordena por popularidade

    nao_indices = [i for i, val in enumerate(dados[coluna]) if val == 'FALSE']
    nao_ordenados = sorted(nao_indices, 
                          key=lambda i: dados['track_popularity'][i], 
                          reverse=True)[:10]
    
    for i, idx in enumerate(nao_ordenados, 1):
        nome = dados['track_name'][idx][:42]
        artista = dados['artist_name'][idx][:23]
        pop = dados['track_popularity'][idx]
        print(f"{i:3} {nome:45} {artista:25} {pop:5.0f}")
    
    # 7. ANÁLISE POR ARTISTA (TOP EXPLÍCITOS)

    print("\n ARTISTAS COM MAIS MÚSICAS EXPLÍCITAS:")
    print("-" * 50)
    
    # Conta músicas explícitas por artista

    artistas_exp = {}
    for i, val in enumerate(dados[coluna]):
        if val == 'TRUE':
            artista = dados['artist_name'][i]
            artistas_exp[artista] = artistas_exp.get(artista, 0) + 1
    
    top_artistas_exp = sorted(artistas_exp.items(), key=lambda x: x[1], reverse=True)[:10]
    
    print(f"{'#':3} {'Artista':40} {'Músicas Exp':12} {'% do total':10}")
    print("-" * 65)
    for i, (artista, qtd) in enumerate(top_artistas_exp, 1):
        perc = (qtd / explicitas * 100) if explicitas else 0
        print(f"{i:3} {artista[:40]:40} {qtd:12} {perc:9.1f}%")
    
    # 8. ANÁLISE POR ARTISTA (MENOS EXPLÍCITOS)
    
    print("\n ARTISTAS SEM MÚSICAS EXPLÍCITAS (TOP 10 POR MÚSICAS):")
    print("-" * 50)
    
    # Artistas sem nenhuma música explícita
    artistas_sem_exp = {}
    for artista in set(dados['artist_name']):
        artistas_sem_exp[artista] = 0
    
    for i, val in enumerate(dados[coluna]):
        artista = dados['artist_name'][i]
        if val == 'TRUE':
            artistas_sem_exp[artista] = artistas_sem_exp.get(artista, 0) + 1
    
    # Filtra só os que tem 0 explícitas
    sem_exp = [(a, dados['artist_name'].count(a)) 
               for a, qtd in artistas_sem_exp.items() 
               if qtd == 0 and dados['artist_name'].count(a) >= 5]
    
    sem_exp.sort(key=lambda x: x[1], reverse=True)
    
    for i, (artista, total) in enumerate(sem_exp[:10], 1):
        print(f"{i:3} {artista[:45]:45} : {total} músicas (nenhuma explícita)")
    
def main():
    """Função principal que executa a análise"""
    
    print("=" * 60)
    print("🔞 ANÁLISE DE CONTEÚDO EXPLÍCITO - SPOTIFY DATASET")
    print("=" * 60)
    
    # Carregar dados
    dados, stats = carregar_dados()
    
    if not dados or not stats:
        print("\n❌ Não foi possível carregar os dados.")
        return
    
    # Executar análise
    resultados = analisar_explicit(stats, dados)
    
    print("\n" + "=" * 60)
    print("✅ ANÁLISE DE CONTEÚDO EXPLÍCITO CONCLUÍDA!")
    print("=" * 60)

# Permite executar este arquivo diretamente
if __name__ == "__main__":
    main()