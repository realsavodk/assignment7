import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd

world_cup = pd.DataFrame({
    "year": [1930, 1934, 1938, 1950, 1954, 1958, 1962, 1966, 1970, 1974, 1978, 1982, 1986, 1990, 1994, 1998, 2002, 2006, 2010, 2014, 2018, 2022], 
    "winner": ["Uruguay", "Italy", "Italy", "Uruguay", "Germany", "Brazil", "Brazil", "England", "Brazil", "Germany", "Argentina", "Italy", "Argentina", "Germany", "Brazil", "France", "Brazil", "Italy", "Spain", "Germany", "France", "Argentina"],
    "runner_up": ["Argentina", "Czechoslovakia", "Hungary", "Brazil", "Hungary", "Sweden", "Czechoslovakia", "Germany", "Italy", "Netherlands", "Netherlands", "Germany", "Germany", "Argentina", "Italy", "Brazil", "Germany", "France", "Netherlands", "Argentina", "Croatia", "France"]
})

# Count wins per country
win_counts = world_cup["winner"].value_counts().reset_index()
win_counts.columns = ["Country", "Wins"]

# Dash App Setup
app = dash.Dash(__name__)

server = app.server
app.layout = html.Div([
    html.H1("FIFA World Cup Winners Dashboard", style={'textAlign': 'center'}),
    
    dcc.Graph(id="world_map"),
    
    # Dropdown to select a country
    html.Label("Select a Country:"),
    dcc.Dropdown(
        id="country_dropdown",
        options=[{"label": c, "value": c} for c in win_counts["Country"].unique()],
        placeholder="Select a country...",
        clearable=True
    ),
    
    # Bar chart showing number of wins
    dcc.Graph(id="wins_chart"),
    
    # Dropdown to select a year
    html.Label("Select a Year:"),
    dcc.Dropdown(
        id="year_dropdown",
        options=[{"label": y, "value": y} for y in world_cup["year"].unique()],
        placeholder="Select a year...",
        clearable=True
    ),
    
    # Display winner and runner-up
    html.Div(id="year_result", style={"fontSize": "20px", "marginTop": "20px"})
])

@app.callback(
    Output("world_map", "figure"),
    Input("country_dropdown", "value")
)
def update_map(selected_country):
    filtered_df = world_cup if selected_country is None else world_cup[world_cup["winner"] == selected_country]
    
    fig = px.choropleth(
        filtered_df,
        locations="winner",
        locationmode="country names",
        color="year",
        color_continuous_scale="Viridis",
        title="World Cup Winners"
    )
    return fig

@app.callback(
    Output("wins_chart", "figure"),
    Input("country_dropdown", "value")
)
def update_wins_chart(selected_country):
    filtered_df = win_counts if selected_country is None else win_counts[win_counts["Country"] == selected_country]
    
    fig = px.bar(
        filtered_df, x="Country", y="Wins",
        title="World Cup Wins by Country",
        color="Wins",
        color_continuous_scale="Blues"
    )
    return fig

@app.callback(
    Output("year_result", "children"),
    Input("year_dropdown", "value")
)
def update_year_result(selected_year):
    if selected_year is None:
        return ""
    result = world_cup[world_cup["year"] == selected_year]
    if result.empty:
        return "No data available."
    return f"Winner: {result.iloc[0]['winner']}, Runner-up: {result.iloc[0]['runner_up']}"

if __name__ == "__main__":
    app.run(debug=True, port=8051)
