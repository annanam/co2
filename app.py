import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html

# Load dataset
file_path = "co2_gdp_merged.csv"  # Ensure this file is uploaded to Render
merged_data = pd.read_csv(file_path)

# Drop rows with missing values
merged_data.dropna(subset=["GDP_Value", "co2_per_capita"], inplace=True)

# Get top 10 CO₂ emitting countries (latest available year)
latest_year = merged_data["Year"].max()
top_co2_emitters = (
    merged_data[merged_data["Year"] == latest_year]
    .nlargest(10, "co2")
)

# Initialize Dash app
app = Dash(__name__)

# Define app layout
app.layout = html.Div([
    html.H1("Global CO₂ Emissions and GDP Dashboard", style={'textAlign': 'center', 'fontFamily': 'Arial'}),

    # Scatter Plot: CO2 Emissions vs GDP
    dcc.Graph(
        id='co2-vs-gdp',
        figure=px.scatter(
            merged_data, x="GDP_Value", y="co2_per_capita", 
            color="Country Name", hover_name="Country Name",
            title="CO₂ Emissions Per Capita vs GDP",
            labels={"GDP_Value": "GDP (USD)", "co2_per_capita": "CO₂ Emissions Per Capita (Metric Tons)"},
            template="plotly_white",
            log_x=True
        )
    ),

    # Line Chart: CO₂ Emissions Over Time
    dcc.Graph(
        id='co2-trends',
        figure=px.line(
            merged_data, x="Year", y="co2_per_capita", 
            color="Country Name", hover_name="Country Name",
            title="CO₂ Emissions Per Capita Over Time",
            labels={"Year": "Year", "co2_per_capita": "CO₂ Emissions Per Capita (Metric Tons)"},
            template="plotly_white"
        )
    ),

    # Bar Chart: Top 10 CO₂ Emitting Countries
    dcc.Graph(
        id='top-co2-emitters',
        figure=px.bar(
            top_co2_emitters, x="Country Name", y="co2",
            title=f"Top 10 CO₂ Emitting Countries in {latest_year}",
            labels={"Country Name": "Country", "co2": "Total CO₂ Emissions (Million Metric Tons)"},
            template="plotly_white"
        )
    )
])

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0", port=8080)
