import pandas as pd
import geopandas as gpd
import plotly.express as px
import plotly.io as pio
import classification_function

#reads the election data csv file (called results.csv) using pandas(pd)
data = pd.read_csv('results.csv')

#creates a new column in the table / dataframe called Member name which combines the Member of parliment's first and sur names
data['Member name'] = data['Member first name'] + ' ' + data['Member surname']
#creates a new column in the table / dataframe called winning party by applying the top_five_parties function to every entry in the First party column
data["winning party"] = data['First party'].apply(classification_function.classify)
#stores the read and converted measurment shapefile of the constituencies to a variable called shape using geopandas(gpd)
shape = gpd.read_file('constituency_shapefile').to_crs("epsg:4326")

#python dictionary of the parties and their corresponding colours - to be used later for the colour distinctive map (so each party comes up as their colour)
party_colours = {
    "Lab": "red",
    "Con": "blue",
    "LD": "orange",
    "SNP": "yellow",
    "SF": "green",
    "OTHER": "grey"
}

#creates a choropleth map using plotly (px) and stores it to a variable called fig
fig = px.choropleth(data,#the csv file that has been read using pandas(pd)
                    geojson=shape,#the shapefile that has been read with geopandas(gpd)
                    locations='ONS ID',#a coloumn of the table / dataframe which holds a unique location ID
                    color='winning party',#makes the thing that determines the colour of each constituency the value in that row of the winning party column in the table / dataframe
                    featureidkey="properties.PCON24CD",#sets the featureidkey to the PCON24CD section of properties - i am not really sure
                    hover_data=["Constituency name", "Member name", "Result"],#displays these extra pieces of inforamtion when you hover over each constituency in the map
                    projection="mercator",#not really sure - just got from the plotly documentaion
                    color_discrete_map=party_colours)#uses the python dictionary party_colours to set the specific colours for each party

fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})#not really sure - just got from the plotly documentation

# Improve the legend (not really sure - just got from the plotly documentation)
fig.update_layout(coloraxis_colorbar=dict(
    thicknessmode="pixels", thickness=0.1,
    lenmode="pixels", len=150,
    yanchor="top", y=0.8,
    ticks="outside", ticksuffix=" %",
    dtick=5
))
fig.update_geos(fitbounds="locations", visible=False)#not really sure - just got from the plotly documentation
pio.write_html(fig, 'templates/plot.html', auto_open=True)#uses plotly.io(pio) to write the map (fig) to an html file in templates called plot and automatically opens it when the code is run