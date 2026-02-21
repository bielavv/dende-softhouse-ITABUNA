
import sys
import os

# Adiciona a pasta principal ao path

pasta_principal = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(pasta_principal)

# Importa a função de carregar dados

from analise_exploratoria.carregar_dados import carregar_dados

def analisar_popularidade(stats, dados):

    print("\n" + "=" * 60)
    print(" ANÁLISE DE POPULARIDADE DAS MÚSICAS")
    print("=" * 60)
    
    coluna = 'track_popularity'
    
    # 1. ESTATÍSTICAS BÁSICAS

    print("\n ESTATÍSTICAS BÁSICAS:")
    print("-" * 40)
    
    media = stats.mean(coluna)
    mediana = stats.median(coluna)
    moda = stats.mode(coluna)
    variancia = stats.variance(coluna)
    desvio = stats.stdev(coluna)
    
    print(f"Média: {media:.1f}")
    print(f"Mediana: {mediana:.1f}")
    print(f"Moda: {moda}")
    print(f"Variância: {variancia:.2f}")
    print(f"Desvio padrão: {desvio:.1f}")
    
    # 2. VALORES MÍNIMO E MÁXIMO
    print("\nEXTREMOS:")
    print("-" * 40)
    
    pop_min = min(dados[coluna])
    pop_max = max(dados[coluna])
    
    print(f"Menor popularidade: {pop_min:.0f}")
    print(f"Maior popularidade: {pop_max:.0f}")
    print(f"Amplitude: {pop_max - pop_min:.0f}")
    
    # 3. QUARTIS
    print("\n QUARTIS:")
    print("-" * 40)
    
    quartis = stats.quartiles(coluna)
    print(f"Q1 (25%): {quartis['Q1']:.1f}")
    print(f"Q2 (50%): {quartis['Q2']:.1f}")
    print(f"Q3 (75%): {quartis['Q3']:.1f}")
    print(f"AIQ (Q3-Q1): {quartis['Q3'] - quartis['Q1']:.1f}")
    
    # 4. DISTRIBUIÇÃO POR FAIXAS
    print("\n DISTRIBUIÇÃO POR POPULARIDADE:")
    print("-" * 40)
    
    # Criar faixas manualmente (0-20, 20-40, 40-60, 60-80, 80-100)

    faixas = [
        (0, 20, "0-20   "),
        (20, 40, "20-40  "),
        (40, 60, "40-60  "),
        (60, 80, "60-80  "),
        (80, 100, "80-100 ")
    ]
    
    contagens = {desc: 0 for _, _, desc in faixas}
    
    for pop in dados[coluna]:
        for min_val, max_val, desc in faixas:
            if min_val <= pop < max_val:
                contagens[desc] += 1
                break
        if pop == 100: 
            contagens["80-100 "] += 1
    
    total = len(dados[coluna])
    for desc, contagem in contagens.items():
        percentual = (contagem / total) * 100
        barra = '█' * int(percentual / 2)
        print(f"{desc}: {contagem:4d} músicas ({percentual:5.1f}%) {barra}")
    
    # 5. TOP 10 MÚSICAS MAIS POPULARES

    print("\n TOP 10 MÚSICAS MAIS POPULARES:")
    print("-" * 50)
    print(f"{'#':3} {'Música':45} {'Artista':25} {'Pop':5}")
    print("-" * 50)
    
    # Ordena por popularidade (decrescente)

    indices = sorted(range(len(dados[coluna])), 
                     key=lambda i: dados[coluna][i], 
                     reverse=True)[:10]
    
    for i, idx in enumerate(indices, 1):
        nome = dados['track_name'][idx][:42]
        artista = dados['artist_name'][idx][:23]
        pop = dados[coluna][idx]
        print(f"{i:3} {nome:45} {artista:25} {pop:5.0f}")
    
    # 6. MÚSICAS MENOS POPULARES

    print("\n TOP 10 MÚSICAS MENOS POPULARES:")
    print("-" * 50)
    print(f"{'#':3} {'Música':45} {'Artista':25} {'Pop':5}")
    print("-" * 50)
    
    indices = sorted(range(len(dados[coluna])), 
                     key=lambda i: dados[coluna][i])[:10]
    
    for i, idx in enumerate(indices, 1):
        nome = dados['track_name'][idx][:42]
        artista = dados['artist_name'][idx][:23]
        pop = dados[coluna][idx]
        print(f"{i:3} {nome:45} {artista:25} {pop:5.0f}")
    
    # 7. POPULARIDADE POR ARTISTA (TOP 10)

    print("\n TOP 10 ARTISTAS POR POPULARIDADE MÉDIA:")
    print("-" * 60)
    print(f"{'#':3} {'Artista':35} {'Músicas':8} {'Pop Média':10} {'Pop Max':8}")
    print("-" * 60)
    
    # Agrupa por artista

    artistas = {}
    for i, artista in enumerate(dados['artist_name']):
        if artista not in artistas:
            artistas[artista] = {
                'musicas': [],
                'total_pop': 0,
                'count': 0,
                'max_pop': 0
            }
        pop = dados[coluna][i]
        artistas[artista]['musicas'].append(pop)
        artistas[artista]['total_pop'] += pop
        artistas[artista]['count'] += 1
        if pop > artistas[artista]['max_pop']:
            artistas[artista]['max_pop'] = pop
    
    # Calcula média e ordena

    artistas_media = []
    for artista, info in artistas.items():
        if info['count'] >= 5:  # Só artistas com pelo menos 5 músicas
            media = info['total_pop'] / info['count']
            artistas_media.append((artista, media, info['count'], info['max_pop']))
    
    artistas_media.sort(key=lambda x: x[1], reverse=True)
    
    for i, (artista, media, qtd, max_pop) in enumerate(artistas_media[:10], 1):
        print(f"{i:3} {artista[:35]:35} {qtd:8} {media:10.1f} {max_pop:8.0f}")
    
    # 9. INSIGHTS

    print("\nINSIGHTS SOBRE POPULARIDADE:")
    print("-" * 40)
    
    print(f"• A popularidade média das músicas é {media:.1f} (escala 0-100)")
    print(f"• Metade das músicas tem popularidade entre {quartis['Q1']:.1f} e {quartis['Q3']:.1f}")
    print(f"• {contagens['80-100 ']} músicas atingiram popularidade máxima (80-100)")
    
    if media > mediana:
        print("• Distribuição assimétrica à esquerda (muitas músicas muito populares)")
    elif media < mediana:
        print("• Distribuição assimétrica à direita (muitas músicas pouco populares)")
    
    # Artista mais popular

    top_artista = artistas_media[0][0]
    top_media = artistas_media[0][1]
    print(f"• Artista com maior popularidade média: {top_artista} ({top_media:.1f})")
    
    # Música mais popular

    idx_top = indices[0]
    print(f"• Música mais popular: '{dados['track_name'][idx_top]}' - {dados['artist_name'][idx_top]}")
    
    return {
        'media': media,
        'mediana': mediana,
        'desvio': desvio,
        'q1': quartis['Q1'],
        'q3': quartis['Q3'],
        'top_musica': dados['track_name'][indices[0]] if indices else None,
        'top_artista': artistas_media[0][0] if artistas_media else None
    }

def main():
    
    print("=" * 60)
    print(" ANÁLISE DE POPULARIDADE - SPOTIFY DATASET")
    print("=" * 60)
    
    # Carregar dados

    dados, stats = carregar_dados()
    
    if not dados or not stats:
        print("\n Não foi possível carregar os dados.")
        return
    
    # Executar análise

    resultados = analisar_popularidade(stats, dados)
    
    print("\n" + "=" * 60)
    print(" ANÁLISE DE POPULARIDADE CONCLUÍDA!")
    print("=" * 60)

# Permite executar este arquivo diretamente

if __name__ == "__main__":
    main()