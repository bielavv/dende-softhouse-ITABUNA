import sys
import os

# Adiciona a pasta principal ao path

pasta_principal = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(pasta_principal)

# Importa a função de carregar dados
from analise_exploratoria.carregar_dados import carregar_dados

def analisar_duracao(stats, dados):
    
    print("\n" + "=" * 60)
    print(" ANÁLISE DE DURAÇÃO DAS MÚSICAS")
    print("=" * 60)
    
    coluna = 'track_duration_min'
    
    # 1. ESTATÍSTICAS BÁSICAS

    print("\n ESTATÍSTICAS BÁSICAS:")
    print("-" * 40)
    
    media = stats.mean(coluna)
    mediana = stats.median(coluna)
    moda = stats.mode(coluna)
    variancia = stats.variance(coluna)
    desvio = stats.stdev(coluna)
    
    print(f"Média: {media:.2f} minutos")
    print(f"Mediana: {mediana:.2f} minutos")
    print(f"Moda: {moda}")
    print(f"Variância: {variancia:.4f}")
    print(f"Desvio padrão: {desvio:.2f} minutos")
    
    # 2. VALORES MÍNIMO E MÁXIMO

    print("\n EXTREMOS:")
    print("-" * 40)
    
    duracao_min = min(dados[coluna])
    duracao_max = max(dados[coluna])
    
    print(f"Menor duração: {duracao_min:.2f} minutos")
    print(f"Maior duração: {duracao_max:.2f} minutos")
    print(f"Amplitude: {duracao_max - duracao_min:.2f} minutos")
    
    # 3. QUARTIS

    print("\nQUARTIS:")
    print("-" * 40)
    
    quartis = stats.quartiles(coluna)
    print(f"Q1 (25%): {quartis['Q1']:.2f} minutos")
    print(f"Q2 (50%): {quartis['Q2']:.2f} minutos")
    print(f"Q3 (75%): {quartis['Q3']:.2f} minutos")
    print(f"AIQ (Q3-Q1): {quartis['Q3'] - quartis['Q1']:.2f} minutos")
    
    # 4. HISTOGRAMA

    print("\n DISTRIBUIÇÃO (HISTOGRAMA):")
    print("-" * 40)
    
    histograma = stats.histogram(coluna, bins=6)
    
    for intervalo, contagem in histograma.items():
        percentual = (contagem / len(dados[coluna])) * 100
        barra = '█' * int(percentual / 2)
        print(f"{intervalo[0]:4.1f} - {intervalo[1]:4.1f}: {contagem:4d} músicas ({percentual:5.1f}%) {barra}")
    
    # 5. MÚSICAS MAIS LONGAS E MAIS CURTAS

    print("\n TOP 5 MÚSICAS MAIS CURTAS:")
    print("-" * 40)
    
    # Ordena por duração (crescente)
    
    indices_curtas = sorted(range(len(dados[coluna])), key=lambda i: dados[coluna][i])[:5]
    
    for i, idx in enumerate(indices_curtas, 1):
        nome = dados['track_name'][idx]
        artista = dados['artist_name'][idx]
        duracao = dados[coluna][idx]
        print(f"{i}. {nome[:40]:40} - {artista[:20]:20} ({duracao:.2f} min)")
    
    print("\n TOP 5 MÚSICAS MAIS LONGAS:")
    print("-" * 40)
    
    # Ordena por duração (decrescente)
    indices_longas = sorted(range(len(dados[coluna])), 
                           key=lambda i: dados[coluna][i], 
                           reverse=True)[:5]
    
    for i, idx in enumerate(indices_longas, 1):
        nome = dados['track_name'][idx]
        artista = dados['artist_name'][idx]
        duracao = dados[coluna][idx]
        print(f"{i}. {nome[:40]:40} - {artista[:20]:20} ({duracao:.2f} min)")
    
    # 6. CATEGORIZAÇÃO POR DURAÇÃO

    print("\n CATEGORIZAÇÃO POR DURAÇÃO:")
    print("-" * 40)
    
    curtos = 0
    medios = 0
    longos = 0
    muito_longos = 0
    
    for duracao in dados[coluna]:
        if duracao < 2:
            curtos += 1
        elif duracao < 3:
            medios += 1
        elif duracao < 5:
            longos += 1
        else:
            muito_longos += 1
    
    total = len(dados[coluna])

    print(f"Músicas curtas (< 2 min):    {curtos:4d} ({curtos/total*100:5.1f}%)")
    print(f"Músicas médias (2-3 min):    {medios:4d} ({medios/total*100:5.1f}%)")
    print(f"Músicas longas (3-5 min):    {longos:4d} ({longos/total*100:5.1f}%)")
    print(f"Músicas muito longas (>5 min): {muito_longos:4d} ({muito_longos/total*100:5.1f}%)")
    
    # 7. INSIGHTS

    print("\n INSIGHTS SOBRE DURAÇÃO:")
    print("-" * 40)
    
    print(f"• A maioria das músicas tem entre {quartis['Q1']:.1f} e {quartis['Q3']:.1f} minutos")
    print(f"• A duração típica (mediana) é de {mediana:.2f} minutos")
    print(f"• A variação média (desvio padrão) é de {desvio:.2f} minutos")
    
    if media > mediana:
        print("• Distribuição assimétrica à direita (algumas músicas muito longas puxam a média para cima)")
    elif media < mediana:
        print("• Distribuição assimétrica à esquerda (muitas músicas curtas)")
    else:
        print("• Distribuição simétrica")
    
    # Retorna as estatísticas principais para uso posterior

    return {
        'media': media,
        'mediana': mediana,
        'desvio': desvio,
        'q1': quartis['Q1'],
        'q3': quartis['Q3']
    }

def main():
    
    print("=" * 60)
    print(" ANÁLISE DE DURAÇÃO - SPOTIFY DATASET")
    print("=" * 60)
    
    # Carregar dados

    dados, stats = carregar_dados()
    
    if not dados or not stats:
        print("\n Não foi possível carregar os dados.")
        return
    
    # Executar análise

    resultados = analisar_duracao(stats, dados)
    
    print("\n" + "=" * 60)
    print(" ANÁLISE DE DURAÇÃO CONCLUÍDA!")
    print("=" * 60)

# Permite executar este arquivo diretamente

if __name__ == "__main__":
    main()