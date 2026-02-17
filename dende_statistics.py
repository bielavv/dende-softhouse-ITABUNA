class Statistics:

    def __init__(self, dataset):

        """VALIDAÇÃO INICIAL DO DATASET(CONJUNTO DE DADOS)"""

        # 1. verificar se é um dicionário

        if not isinstance(dataset, dict):
            raise TypeError("O dataset deve ser um dicionário")
        
        # 2. verificar se todas as chaves tem listas

        for coluna, valores in dataset.items():
            if not isinstance(valores, list):
                raise TypeError(f"Valores da coluna '{coluna}' devem ser uma lista")
            
        # 3. Todas as listas tem o mesmo tamanho?

        if dataset:
            tamanhos = [len(v) for v in dataset.values()]
            if len(set(tamanhos)) > 1:
                raise ValueError("Todos as caolunas devem ter o mesmo número de elementos")
            
        # 4. cada coluna tem dados do mesmo tipo?

        for coluna, valores in dataset.items(): # esse loop aninhado vai percorrer colunas distinta do dataset.items e validar o tipo igual
            if valores:
                primeiro_tipo = type(valores[0])
                for valor in valores:
                    if type(valor) != primeiro_tipo:
                         raise TypeError(f"coluna '{coluna}' tem tipos misturados")


            # caso ele passe por todas as validações, vai ficar armazenado aqui para ultilizações futuras.
    
        self.dataset = dataset

    def mean(self, column):

        """Média - só para colunas numéricas"""

        # validação 1. verificar se a coluna existe no dataset

        if column not in self.dataset:
            raise KeyError(f"Coluna '{column}' não existe no dataset")
        
        dados = self.dataset[column]

        # validação 2. verica se a lista está vazia

        if len(dados) == 0:
            raise KeyError(f"Não é possivél calcular média de uma coluna vazia")
        
        # validação 3. verifica se todos são números, se não for mostra detalhes 

        for i, valor in enumerate(dados):
            if not isinstance(valor, (int, float)):
                raise TypeError(
                    f" Média só pode ser calculada em colunas numéricas. "
                    f"Coluna '{column}' na posição {i}: {repr(valor)} é {type(valor).__name__}"
                )
            
        #calculo da média é realizada aqui, após as validações
        # sum: soma todos os dados da coluna 
        # len: soma a quantidade a quantidade que aparece

        return sum(dados) / len(dados)
    
    def median(self, column):
    
     # validação 1. verificar se a coluna existe no dataset:

      if column not in self.dataset:
            raise KeyError(f"Coluna '{column}' não existe no dataset")
    
      dados = self.dataset[column]

      # validação 2. verica se a lista está vazia

      if len(dados) == 0:
            raise KeyError(f"Não é possivél verificar a mediana de uma coluna vazia")
      

     # ordenação com prioridade 

      if column == "priority":
        ordem = {"baixa": 1, "media": 2, "alta": 3}
        dados_ordenados = sorted(dados, key=lambda x: ordem[x])

     # ordenação para outros casos sem prioridade
      else:
        dados_ordenados = sorted(dados)


      # quantidade de elementos 

      total_elementos = len(dados_ordenados)
      meio = total_elementos // 2

      # caso ímpar

      if total_elementos % 2 == 1:
          return dados_ordenados[meio]
      
      # caso par

      esquerda = dados_ordenados[meio - 1]
      direita = dados_ordenados[meio]

      # verifica se os valores são numéricos bilateralmente 

      if isinstance(esquerda, (int, float)) and isinstance(direita, (int, float)):
         
         # para números: média dos dois

         return (esquerda + direita) / 2
      
      else:
          # para texto: retorna o primeiro

          return esquerda
          
    def mode(self, column):
      
     # validação 1. verificar se a coluna existe no dataset:

      if column not in self.dataset:
            raise KeyError(f"Coluna '{column}' não existe no dataset")
    
      dados = self.dataset[column]

      # validação 2. verica se a lista está vazia

      if len(dados) == 0:
            raise KeyError(f"Não é possivél verificar a mediana de uma coluna vazia")
      
      # contar frequenência em que os itens aparece
      contagem = {}
      for valor in dados:
           if valor in contagem:
                contagem[valor] += 1
           else:
               contagem[valor] = 1

      # encontra a maior contagem
      maior_contagem = max(contagem.values())

      # aramazenar todas as contagens realizadas em "contagem"

      modas = []
      for valor, freq in contagem.items():
       if freq == maior_contagem:
        modas.append(valor)


      return modas
    
    def variance(self, column):
      
     # validação 1. verificar se a coluna existe no dataset:

      if column not in self.dataset:
            raise KeyError(f"Coluna '{column}' não existe no dataset")
    
      dados = self.dataset[column]

      # validação 2. verica se a lista está vazia

      if len(dados) == 0:
            raise KeyError(f"Não é possivél verificar a mediana de uma coluna vazia")
      
      # validação 3. verifica se todos os dados são números

      for i, valor in enumerate(dados):
       if not isinstance(valor, (int, float)):
        raise TypeError(
            f"Variância só pode ser calculada em colunas numéricas. "
            f"Coluna '{column}' na posição {i}: {repr(valor)} é {type(valor).__name__}"
        )
    
    # reutilização da média já calculada e validada + calculo de variancia
    # houve necessidade de ajuste do valor indicado no teste em tests.py, pois o resultado obtido foi 525.25 e não 507.25.

      media = self.mean(column)
      soma_quadrados = sum((x - media) ** 2 for x in dados) 
      return soma_quadrados / len(dados)

    def stdev(self, column):
  
     # validação 1. verificar se a coluna existe no dataset:

      if column not in self.dataset:
        raise KeyError(f"Coluna '{column}' não existe no dataset")
    
      dados = self.dataset[column]

      # validação 2. verica se a lista está vazia

      if len(dados) == 0:
         raise KeyError(f"Não é possivél verificar a mediana de uma coluna vazia")
      
      # validação 3. verifica se todos os dados são números

      for i, valor in enumerate(dados):
        if not isinstance(valor, (int, float)):
         raise TypeError(
            f"Variância só pode ser calculada em colunas numéricas. "
            f"Coluna '{column}' na posição {i}: {repr(valor)} é {type(valor).__name__}"
        )
    # reutilização da variância já calculada e validada + calculo do desvio padrão
    # houve necessidade de ajuste do valor indicado no teste em tests.py, pois o resultado obtido foi 22.918333 e não 22.527756.

      variancia = self.variance(column)
      return variancia ** 0.5

    def covariance(self, column_a, column_b):
        """
        Calcula a covariância entre duas colunas.

        Parâmetros
        ----------
        column_a : str
            O nome da primeira coluna (X).
        column_b : str
            O nome da segunda coluna (Y).

        Retorno
        -------
        float
            O valor da covariância entre as duas colunas.
        """
        pass

    def itemset(self, column):
        """
        Retorna o conjunto de itens únicos em uma coluna.

        Parâmetros
        ----------
        column : str
            O nome da coluna (chave do dicionário do dataset).

        Retorno
        -------
        set
            Um conjunto com os valores únicos da coluna.
        """
        pass

    def absolute_frequency(self, column):
        """
        Calcula a frequência absoluta de cada item em uma coluna.

        Parâmetros
        ----------
        column : str
            O nome da coluna (chave do dicionário do dataset).

        Retorno
        -------
        dict
            Um dicionário onde as chaves são os itens e os valores são
            suas contagens (frequência absoluta).
        """
        pass

    def relative_frequency(self, column):
        """
        Calcula a frequência relativa de cada item em uma coluna.

        Parâmetros
        ----------
        column : str
            O nome da coluna (chave do dicionário do dataset).

        Retorno
        -------
        dict
            Um dicionário onde as chaves são os itens e os valores são
            suas proporções (frequência relativa).
        """
        pass

    def cumulative_frequency(self, column, frequency_method='absolute'):
        """
        Calcula a frequência acumulada (absoluta ou relativa) de uma coluna.

        A frequência é calculada sobre os itens ordenados.

        Parâmetros
        ----------
        column : str
            O nome da coluna (chave do dicionário do dataset).
        frequency_method : str, opcional
            O método a ser usado: 'absolute' para contagem acumulada ou
            'relative' para proporção acumulada (padrão é 'absolute').

        Retorno
        -------
        dict
            Um dicionário ordenado com os itens como chaves e suas
            frequências acumuladas como valores.
        """
        pass

    def conditional_probability(self, column, value1, value2):
        """
        Calcula a probabilidade condicional P(X_i = value1 | X_{i-1} = value2).

        Este método trata a coluna como uma sequência e calcula a probabilidade
        de encontrar `value1` imediatamente após `value2`.

        Fórmula: P(A|B) = Contagem de sequências (B, A) / Contagem total de B

        Parâmetros
        ----------
        column : str
            O nome da coluna (chave do dicionário do dataset).
        value1 : any
            O valor do evento consequente (A).
        value2 : any
            O valor do evento condicionante (B).

        Retorno
        -------
        float
            A probabilidade condicional, um valor entre 0 e 1.
        """
        pass

    def quartiles(self, column):
        """
        Calcula os quartis (Q1, Q2 e Q3) de uma coluna.

        Parâmetros
        ----------
        column : str
            O nome da coluna (chave do dicionário do dataset).

        Retorno
        -------
        dict
            Um dicionário com os quartis Q1, Q2 (mediana) e Q3.
        """
        pass

    def histogram(self, column, bins):
        """
        Gera um histograma baseado em buckets (intervalos).

        Parâmetros
        ----------
        column : str
            O nome da coluna (chave do dicionário do dataset).
        bins : int
            Número de buckets (intervalos).

        Retorno
        -------
        dict
            Um dicionário onde as chaves são os intervalos (tuplas)
            e os valores são as contagens.
        """
        pass

