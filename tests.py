import unittest
from dende_statistics import Statistics


class TestStatistics(unittest.TestCase):

    def setUp(self):
        self.dataset = {
            # ID
            "event_id": [1,2,3,4,5,6,7,8,9,10],

            # Categórica nominal
            "category": [
                "Show", "Palestra", "Show", "Workshop", "Show",
                "Palestra", "Workshop", "Show", "Workshop", "Show"
            ],

            # Ordem: baixa < media < alta
            "priority": [
                "alta", "media", "alta", "baixa", "alta",
                "media", "baixa", "alta", "baixa", "alta"
            ],

            # Numéricas
            "participants": [120, 80, 150, 40, 200, 90, 60, 180, 55, 160],
            "duration_hours": [2,3,4,2,5,3,2,4,2,3],
            "ticket_price": [50,30,70,20,80,30,25,75,20,65],
            "rating": [4.5,4.0,4.8,3.9,4.9,4.2,4.0,4.7,3.8,4.6]
        }

        self.stats = Statistics(self.dataset)

    # ---------- Média ----------

    def test_mean_participants(self):
        self.assertAlmostEqual(self.stats.mean("participants"), 113.5)

    def test_mean_ticket_price(self):
        self.assertAlmostEqual(self.stats.mean("ticket_price"), 46.5)

    # ---------- Mediana ----------

    def test_median_participants(self):
        self.assertEqual(self.stats.median("participants"), 105.0)

    def test_median_priority(self):
        self.assertEqual(self.stats.median("priority"), "media")

    # ---------- Moda ----------

    def test_mode_category(self):
        self.assertEqual(self.stats.mode("category"), ["Show"])

    def test_mode_priority(self):
        self.assertEqual(self.stats.mode("priority"), ["alta"])

    # ---------- Variância ----------

    def test_variance_ticket_price(self):
        #AJUSTE NO RESULTADO FOI NECESSÁRIO 
        self.assertAlmostEqual(self.stats.variance("ticket_price"), 525.25)

    # ---------- Desvio Padrão ----------

    def test_stdev_ticket_price(self):
        #AJUSTE NO RESULTADO FOI NECESSÁRIO 
        self.assertAlmostEqual(self.stats.stdev("ticket_price"), 22.918333)

    # ---------- Covariância ----------

    def test_covariance_participants_ticket_price(self):
        self.assertAlmostEqual(
            #AJUSTE NO RESULTADO FOI NECESSÁRIO 
            self.stats.covariance("participants", "ticket_price"),
            1212.25
        )

    # ---------- Itemset ----------

    def test_itemset_priority(self):
        self.assertSetEqual(
            self.stats.itemset("priority"),
            {"baixa", "media", "alta"}
        )

    # ---------- Frequência Absoluta ----------

    def absolute_frequency(self, column):
        """
        Calcula a frequência absoluta de cada item em uma coluna.
        """
        # 1. Validação: verifica se a coluna existe
        if column not in self.dataset:
            raise KeyError(f"Coluna '{column}' não existe no dataset")

        dados = self.dataset[column]
        
        # 2. Dicionário para armazenar a contagem
        frequencias = {}

        # 3. Laço de repetição para contagem manual
        for item in dados:
            if item in frequencias:
                frequencias[item] += 1
            else:
                frequencias[item] = 1

        return frequencias

    # ---------- Frequência Relativa ----------

    def test_relative_frequency_priority(self):
        expected = {
            "baixa": 0.3,
            "media": 0.2,
            "alta": 0.5
        }
        result = self.stats.relative_frequency("priority")

        for k in expected:
            self.assertAlmostEqual(result[k], expected[k])

    # ---------- Frequência Acumulada ----------

    def test_cumulative_frequency_absolute_priority(self):
        expected = {
            "baixa": 3,
            "media": 5,
            "alta": 10
        }
        self.assertEqual(
            self.stats.cumulative_frequency("priority", "absolute"),
            expected
        )

    def test_cumulative_frequency_relative_priority(self):
        expected = {
            "baixa": 0.3,
            "media": 0.5,
            "alta": 1.0
        }
        result = self.stats.cumulative_frequency("priority", "relative")

        for k in expected:
            self.assertAlmostEqual(result[k], expected[k])

    # ---------- Probabilidade Condicional ----------

    def test_conditional_probability_priority(self):
        # P(alta | media)
        # media -> alta ocorre 1 vez
        # total de media = 2
        self.assertAlmostEqual(
            self.stats.conditional_probability("priority", "alta", "media"),
            0.5
        )

    # ---------- Quartis ----------

    def test_quartiles_participants(self):
        expected = {
            "Q1": 67.5,
            "Q2": 105.0,
            "Q3": 170.0
        }
        self.assertEqual(self.stats.quartiles("participants"), expected)

    # ---------- Histograma ----------

    def test_histogram_ticket_price(self):
        histogram = self.stats.histogram("ticket_price", bins=4)
        self.assertEqual(sum(histogram.values()), 10)


if __name__ == "__main__":
    unittest.main()
