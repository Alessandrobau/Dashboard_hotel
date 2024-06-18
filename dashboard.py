import pytest
from unittest.mock import MagicMock
from dash_example import update_dynamic_graph

# Mock dos dados para simular as funções de gráfico
graph_options = {
    "Hotel Price Time": MagicMock(),
    "Hotel Price": MagicMock(),
    "Guests Map": MagicMock(),
    "Price Variation": MagicMock(),
    "Total Guests per Month": MagicMock(),
}

def test_update_dynamic_graph():
    # Testar para cada chave em graph_options
    for graph_name, mock_graph in graph_options.items():
        figure, description = update_dynamic_graph(graph_name)

        # Verifica se a figura retornada é o mock correspondente
        assert figure == graph_options[graph_name]

        # Verifica se a descrição retornada é correta
        expected_descriptions = {
            "Hotel Price Time": "Quantidade de reservas por quantidade de dias reservados",
            "Hotel Price": "Preco dos Hoteis conforme o tipo do quarto reservado.",
            "Guests Map": "Distribuição geográfica dos hospedes.",
            "Price Variation": "Variação de preços conforme o mês do ano.",
            "Total Guests per Month": "Número total de Hóspedes por Mês.",
        }
        assert description == expected_descriptions.get(graph_name, "")

if __name__ == "__main__":
    pytest.main()
