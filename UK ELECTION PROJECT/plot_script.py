import pandas as pd
import geopandas as gpd
import plotly.express as px
import plotly.io as pio

data = pd.read_csv('results.csv')


def top_five_parties(placeholder):
    parties_to_look_for = ["Lab", "Con", "LD", "SNP", "SF"]
    if placeholder in parties_to_look_for:
        return placeholder
    else:
        return "OTHER"


data['Member name'] = data['Member first name'] + ' ' + data['Member surname']
data["winning party"] = data['First party'].apply(top_five_parties)
shape = gpd.read_file('constituency_shapefile').to_crs("epsg:4326")

party_colours = {
    "Lab": "red",
    "Con": "blue",
    "LD": "orange",
    "SNP": "yellow",
    "SF": "green",
    "OTHER": "grey"
}

fig = px.choropleth(data,
                    geojson=shape,
                    locations='ONS ID',
                    color='winning party',
                    featureidkey="properties.PCON24CD",
                    hover_data=["Constituency name", "Member name"],
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
pio.write_html(fig, 'templates/plot.html', auto_open=True)