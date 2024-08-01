import pandas as pd
import geopandas as gpd
import plotly.express as px
import plotly.io as pio

data = pd.read_csv('results.csv')


def top_five_parties(placeholder):
    parties_to_look_for = ["Lab", "Con", "LD", "SNP"]
    if placeholder in parties_to_look_for:
        return placeholder
    else:
        return "OTHER"



data["winner"] = data['First party'].apply(top_five_parties)
shape = gpd.read_file('constituency_shapefile').to_crs("epsg:4326")

party_colours = {
    "Lab": "red",
    "Con": "blue",
    "LD": "orange",
    "SNP": "yellow",
    "OTHER": "grey"
}

fig = px.choropleth(data[data["First party"] != "SF"],
                    geojson=shape,
                    locations='ONS ID',
                    color='winner',
                    featureidkey="properties.PCON24CD",
                    hover_data=["Constituency name"],
                    projection="mercator",
                    color_discrete_map=party_colours)

fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

# Improve the legend
fig.update_layout(coloraxis_colorbar=dict(
    thicknessmode="pixels", thickness=0.1,
    lenmode="pixels", len=150,
    yanchor="top", y=0.8,
    ticks="outside", ticksuffix=" %",
    dtick=5
))
fig.update_geos(fitbounds="locations", visible=False)
pio.write_html(fig, 'templates/plot.html', auto_open=False)