from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
from hotel_data import *

app = Dash(__name__)

graph_options = {
    "Hotel Price Time": tempo_estadia,
    "Hotel Price": hotel_price,
    "Guests Map": guests_map,
    "Price Variation": price_variation,
    "Total Guests per Month": total_guests_month,
}

app.layout = html.Div(
    [
        html.H1(
            children="Hotel Dashboard", style={"textAlign": "center", "color": "white"}
        ),
        html.Div(
            [
                html.P(id="graph-description", style={"color": "white"}),
                dcc.Dropdown(
                    options=[{"label": k, "value": k} for k in graph_options.keys()],
                    placeholder="Selecione um gráfico",
                    value="Guests Map",
                    id="graph-dropdown-selection",
                    style={"margin-bottom": "20px"},
                ),
            ],
            style={"margin-bottom": "20px"},
        ),
        dcc.Graph(id="dynamic-graph-content"),
    ],
    style={"backgroundColor": "black", "padding": "20px"},
)


@app.callback(
    [
        Output("dynamic-graph-content", "figure"),
        Output("graph-description", "children"),
    ],
    [Input("graph-dropdown-selection", "value")],
)
def update_dynamic_graph(selected_graph):
    graph_figure = graph_options[selected_graph]

    description = {
        "Hotel Price Time": "Quantidade de reservas por quantidade de dias reservados",
        "Hotel Price": "Preco dos Hoteis conforme o tipo do quarto reservado.",
        "Guests Map": "Distribuição geográfica dos hospedes.",
        "Price Variation": "Variação de preços conforme o mês do ano.",
        "Total Guests per Month": "Número total de Hóspedes por Mês.",
    }.get(selected_graph, "")

    return graph_figure, description


if __name__ == "__main__":
    app.run(debug=True)
