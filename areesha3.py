import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px

app = dash.Dash(__name__)
server = app.server

data_url = "https://raw.githubusercontent.com/pakkhee/DataVisual/main/top50.csv"

# Specify the encoding as ISO-8859-1 (Latin-1)
data = pd.read_csv(data_url, encoding='ISO-8859-1')

# Create a new DataFrame with the count of songs for each artist name
artist_count = data['Artist.Name'].value_counts().reset_index()
artist_count.columns = ['Artist Name', 'Count of Songs']

# Create the figure using Plotly Express for the artist count bar chart
fig_artist_count = px.bar(data_frame=artist_count,
                          x='Artist Name',
                          y='Count of Songs',
                          title="Count of songs for each artist name",
                          labels={'Artist Name': 'Artist Name', 'Count of Songs': 'Count of Songs'})
fig_artist_count.update_layout(xaxis_title_text="", yaxis_title_text="Count of Songs")

# Create the figure using Plotly Express for the Loudness histogram
fig_loudness_histogram = px.histogram(data_frame=data,
                                      x='Loudness..dB..',
                                      nbins=10,
                                      labels={'Loudness..dB..': 'Loudness (dB)', 'count': 'Count'})
fig_loudness_histogram.update_layout(title="Histogram of Loudness (dB)")

# Calculate genre counts and select the top 5 genres
genre_counts = data['Genre'].value_counts().reset_index()
genre_counts.columns = ['Genre', 'Count']
top_5_genre_counts = genre_counts.head(5)

# Create the figure using Plotly Express for the top 5 genres pie chart
fig_top_5_genre_pie = px.pie(data_frame=top_5_genre_counts,
                             names='Genre',
                             values='Count',
                             title="Pie Chart of Top 5 Genres by Count")

# Define the layout of your Dash app
app.layout = html.Div([
    html.H1("Top 50 Songs Dashboard"),
html.H2("Areesha - Assignment 3"),
    
    # Add the artist count bar chart
    dcc.Graph(figure=fig_artist_count, id='artist-count-graph'),

    # Add the Loudness histogram
    dcc.Graph(figure=fig_loudness_histogram, id='loudness-histogram-graph'),

    # Add the top 5 genres pie chart
    dcc.Graph(figure=fig_top_5_genre_pie, id='top-5-genres-pie-chart'),
])

if __name__ == '__main__':
    app.run_server(debug=True)
