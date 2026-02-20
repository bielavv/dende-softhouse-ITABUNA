
import sys
import os

# Adiciona a pasta principal ao path

pasta_principal = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(pasta_principal)

# Importa a função de carregar dados

from analise_exploratoria.carregar_dados import carregar_dados

def analisar_artistas(stats, dados):
    """
    Analisa os artistas do dataset
    """
    print("\n" + "=" * 60)
    print(" ANÁLISE DE ARTISTAS")
    print("=" * 60)
    
    coluna = 'artist_name'
    total_musicas = len(dados[coluna])
    
    # 1. ESTATÍSTICAS BÁSICAS SOBRE ARTISTAS

    print("\n ESTATÍSTICAS GERAIS:")
    print("-" * 40)
    
    artistas_unicos = len(stats.itemset(coluna))
    print(f"Total de artistas diferentes: {artistas_unicos}")
    print(f"Média de músicas por artista: {total_musicas/artistas_unicos:.1f}")
    
    # 2. FREQUÊNCIA ABSOLUTA (TOP 30)

    print("\n TOP 30 ARTISTAS COM MAIS MÚSICAS:")
    print("-" * 70)
    print(f"{'#':3} {'Artista':45} {'Músicas':8} {'%':6} {'Acumulado':9}")
    print("-" * 70)
    
    freq_abs = stats.absolute_frequency(coluna)
    top_artistas = sorted(freq_abs.items(), key=lambda x: x[1], reverse=True)[:30]
    
    acumulado = 0
    for i, (artista, qtd) in enumerate(top_artistas, 1):
        acumulado += qtd
        percentual = (qtd / total_musicas) * 100
        perc_acumulado = (acumulado / total_musicas) * 100
        barra = '█' * int(percentual * 2)
        print(f"{i:3} {artista[:45]:45} {qtd:8} {percentual:5.1f}% {perc_acumulado:6.1f}%  {barra}")
    
    # 3. FREQUÊNCIA RELATIVA (proporção)

    print("\n FREQUÊNCIA RELATIVA (TOP 10):")
    print("-" * 50)
    
    freq_rel = stats.relative_frequency(coluna)
    for i, (artista, qtd) in enumerate(top_artistas[:10], 1):
        proporcao = freq_rel[artista] * 100
        print(f"{i:3} {artista[:40]:40} : {proporcao:5.2f}% do dataset")
    
    # 4. FREQUÊNCIA ACUMULADA

    print("\n FREQUÊNCIA ACUMULADA (TOP 10):")
    print("-" * 50)
    
    freq_acum = stats.cumulative_frequency(coluna)
    for i, (artista, qtd) in enumerate(top_artistas[:10], 1):
        acum = freq_acum[artista]
        perc_acum = (acum / total_musicas) * 100
        print(f"{i:3} {artista[:40]:40} : {acum:5d} músicas ({perc_acum:5.1f}%)")
    
    # 5. DISTRIBUIÇÃO DE PRODUTIVIDADE

    print("\n DISTRIBUIÇÃO DE PRODUTIVIDADE DOS ARTISTAS:")
    print("-" * 50)
    
    # Categorias de produtividade

    categorias = [
        (1, "1 música apenas"),
        (2, "2-5 músicas"),
        (6, "6-10 músicas"),
        (11, "11-20 músicas"),
        (21, "21+ músicas")
    ]
    
    contagens = {cat[1]: 0 for cat in categorias}
    
    for artista, qtd in freq_abs.items():
        if qtd == 1:
            contagens["1 música apenas"] += 1
        elif qtd <= 5:
            contagens["2-5 músicas"] += 1
        elif qtd <= 10:
            contagens["6-10 músicas"] += 1
        elif qtd <= 20:
            contagens["11-20 músicas"] += 1
        else:
            contagens["21+ músicas"] += 1
    
    for categoria, contagem in contagens.items():
        percentual = (contagem / artistas_unicos) * 100
        barra = '█' * int(percentual / 2)
        print(f"{categoria:20}: {contagem:4d} artistas ({percentual:5.1f}%) {barra}")
    
    # 6. TOP 10 ARTISTAS POR LETRA

    print("\n DISTRIBUIÇÃO POR PRIMEIRA LETRA:")
    print("-" * 40)
    
    letras = {}
    for artista in freq_abs.keys():
        if artista and artista[0].isalpha():
            letra = artista[0].upper()
            letras[letra] = letras.get(letra, 0) + 1
    
    top_letras = sorted(letras.items(), key=lambda x: x[1], reverse=True)[:10]
    
    for letra, qtd in top_letras:
        percentual = (qtd / artistas_unicos) * 100
        barra = '█' * int(percentual)
        print(f"Letra '{letra}': {qtd:4d} artistas ({percentual:5.1f}%) {barra}")
    
    # 7. ARTISTAS COM MAIOR E MENOR NÚMERO DE MÚSICAS

    print("\n ARTISTA MAIS PRODUTIVO:")
    print("-" * 40)
    
    top_artista = top_artistas[0][0]
    top_qtd = top_artistas[0][1]
    print(f"{top_artista} - {top_qtd} músicas ")
    
    # Segundo colocado

    if len(top_artistas) > 1:
        segundo = top_artistas[1][0]
        segundo_qtd = top_artistas[1][1]
        print(f"\n Segundo lugar: {segundo} - {segundo_qtd} músicas")
    
    # Terceiro colocado

    if len(top_artistas) > 2:
        terceiro = top_artistas[2][0]
        terceiro_qtd = top_artistas[2][1]
        print(f" Terceiro lugar: {terceiro} - {terceiro_qtd} músicas")
    
    # 8. MÉTRICAS DE CONCENTRAÇÃO

    print("\n MÉTRICAS DE CONCENTRAÇÃO:")
    print("-" * 40)
    
    # Soma das músicas dos top 10

    top10_total = sum(qtd for _, qtd in top_artistas[:10])
    print(f"Top 10 artistas respondem por: {top10_total} músicas ({top10_total/total_musicas*100:.1f}% do total)")
    
    # Soma das músicas dos top 20

    top20_total = sum(qtd for _, qtd in top_artistas[:20])
    print(f"Top 20 artistas respondem por: {top20_total} músicas ({top20_total/total_musicas*100:.1f}% do total)")
    
    # Artistas com apenas 1 música

    artistas_1_musica = contagens["1 música apenas"]
    musicas_1_musica = artistas_1_musica  # Cada um tem 1 música
    print(f"Artistas com apenas 1 música: {artistas_1_musica} ({artistas_1_musica/artistas_unicos*100:.1f}% dos artistas)")
    print(f"Estes representam: {musicas_1_musica/total_musicas*100:.1f}% do total de músicas")
    

def main():
    
    print("=" * 60)
    print("🎤 ANÁLISE DE ARTISTAS - SPOTIFY DATASET")
    print("=" * 60)
    
    # Carregar dados
    dados, stats = carregar_dados()
    
    if not dados or not stats:
        print("\n Não foi possível carregar os dados.")
        return
    
    # Executar análise
    resultados = analisar_artistas(stats, dados)
    
    print("\n" + "=" * 60)
    print("ANÁLISE DE ARTISTAS CONCLUÍDA!")
    print("=" * 60)

# Permite executar este arquivo diretamente
if __name__ == "__main__":
    main()