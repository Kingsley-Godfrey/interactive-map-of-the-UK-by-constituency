import pandas as pd
import geopandas as gpd
import plotly.express as px
import plotly.io as pio
import classification_function

#reads the election data csv file (called results.csv) using pandas(pd)
data = pd.read_csv('results.csv')

#creates a new column in the table / dataframe by appliying the classify fuction held in classification_function to what is in each row of the First party column
data["winner"] = data['First party'].apply(classification_function.classify)

#creates a new coloumn in the table / datafram called voter turnout percentage which holds the percentage of the electorate that voted (determined by adding the valid and invalid votes then dividing it be the electorate and then multiplying by 100 so you get the answer as a percentage)
data['voter turnout percentage'] = ((data['Valid votes'] + data['Invalid votes']) / data['Electorate']) * 100

#uses geopandas(gpd) to read the constituency_shapefile and to convert its measurments
shape = gpd.read_file('constituency_shapefile').to_crs("epsg:4326")

#creates a choropleth map using plotly(px) and stores it to a variable called fig - short for figure
fig = px.choropleth(data,#the csv file that has been read using pandas(pd)
                    geojson=shape,#the constituency_shapefile that has been read and converted by geopandas(gpdP)
                    locations='ONS ID',#the ONS ID column in the table / dataframe
                    color='voter turnout percentage',#sets the thing that determies the colour to the voter turnout percentage column of the table / datframe
                    featureidkey="properties.PCON24CD",#not really sure
                    hover_data=["Constituency name"],#displays the specific constituency name when hovering over a specific constituency in the map
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