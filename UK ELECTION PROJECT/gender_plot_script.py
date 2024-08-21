import pandas as pd
import geopandas as gpd
import plotly.express as px
import plotly.io as pio
import classification_function

data = pd.read_csv('results.csv')

data["winner"] = data['First party'].apply(classification_function.classify)
shape = gpd.read_file('constituency_shapefile').to_crs("epsg:4326")

gender_colours = {
    "Male": "blue",
    "Female": "pink"
}

fig = px.choropleth(data[data["First party"] != "SF"],
                    geojson=shape,
                    locations='ONS ID',
                    color='Member gender',
                    featureidkey="properties.PCON24CD",
                    hover_data=["Constituency name", "First party"],
                    projection="mercator",
                    color_discrete_map=gender_colours)

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
pio.write_html(fig, 'templates/gender_plot.html', auto_open=True)