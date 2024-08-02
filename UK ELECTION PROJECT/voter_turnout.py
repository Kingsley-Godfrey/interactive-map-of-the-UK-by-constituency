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



data["winner"] = data['First party'].apply(top_five_parties)
shape = gpd.read_file('constituency_shapefile').to_crs("epsg:4326")
data['voter turnout'] = (data['Valid votes'] + data['Invalid votes']) / data['Electorate']


fig = px.choropleth(data,
                    geojson=shape,
                    locations='ONS ID',
                    color='voter turnout',
                    featureidkey="properties.PCON24CD",
                    hover_data=["Constituency name"],
                    projection="mercator",
                    color_continuous_scale='Viridis')

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
pio.write_html(fig, 'templates/voter_turnout_plot.html', auto_open=True)