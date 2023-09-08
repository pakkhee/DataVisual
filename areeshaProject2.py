import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px

app = dash.Dash(__name__)
server = app.server

data_url = "https://raw.githubusercontent.com/pakkhee/DataVisual/main/top50.csv"

# Specify the encoding as ISO-8859-1 (Latin-1)
data = pd.read_csv(data_url, encoding="ISO-8859-1")

# Create a new DataFrame with the count of songs for each artist name
artist_count = data["Artist.Name"].value_counts().reset_index()
artist_count.columns = ["Artist Name", "Count of Songs"]

# Select the top 10 artists with the most songs
top_10_artists = artist_count.head(15)

# Create the figure using Plotly Express for the artist count line chart
fig_artist_count = px.line(
    data_frame=top_10_artists,
    x="Artist Name",
    y="Count of Songs",
    title="Count of songs for each artist name",
    labels={"Artist Name": "Artist Name", "Count of Songs": "Count of Songs"},
)
fig_artist_count.update_layout(xaxis_title_text="", yaxis_title_text="Count of Songs")

# Calculate genre counts and select the top 5 genres
genre_counts = data["Genre"].value_counts().reset_index()
genre_counts.columns = ["Genre", "Count"]

# Define the layout of your Dash app
app.layout = html.Div(
    [
        html.H1("Top 50 Songs Dashboard"),
        # Tabs for different charts
        dcc.Tabs(
            id="chart-tabs",
            value="tab-artist-count",
            children=[
                dcc.Tab(
                    label="Artist Count",
                    value="tab-artist-count",
                    children=[
                        html.Div(
                            [
                                html.Label(
                                    "Select Artist(s):", style={"font-weight": "bold"}
                                ),
                                # Checklist to select multiple artists
                                dcc.Checklist(
                                    id="artist-checklist",
                                    options=[
                                        {"label": artist, "value": artist}
                                        for artist in top_10_artists["Artist Name"]
                                    ],
                                    value=[
                                        top_10_artists["Artist Name"].iloc[0]
                                    ],  # Default value
                                    inline=True,  # Arrange items side by side
                                    labelStyle={"margin-right": "10px"},
                                ),
                            ],
                            style={"margin-bottom": "20px"},
                        ),
                        dcc.Graph(id="artist-count-line-chart"),  # Updated graph ID
                    ],
                ),
                dcc.Tab(
                    label="Top 5 Genres",
                    value="tab-top-5-genres",
                    children=[
                        # Radio button to select the number of top genres to show
                        dcc.RadioItems(
                            id="genre-count-radio",
                            options=[
                                {"label": "Show Top 5 Genres", "value": 5},
                                {"label": "Show Top 10 Genres", "value": 10},
                            ],
                            value=5,  # Default value
                            labelStyle={"display": "block"},
                        ),
                        dcc.Graph(id="top-genres-pie-chart"),  # Updated graph ID
                    ],
                ),
            ],
        ),
    ]
)


# Callback to update the artist count line chart based on the selected artists
@app.callback(
    Output("artist-count-line-chart", "figure"), Input("artist-checklist", "value")
)
def update_artist_count_line_chart(selected_artists):
    # Filter the data based on the selected artists
    filtered_data = data[data["Artist.Name"].isin(selected_artists)]

    # Calculate the count of songs for the selected artists
    artist_song_counts = filtered_data["Artist.Name"].value_counts().reset_index()
    artist_song_counts.columns = ["Artist Name", "Count of Songs"]

    # Create the figure using Plotly Express for the artist count line chart
    fig_artist_count = px.line(
        data_frame=artist_song_counts,
        x="Artist Name",
        y="Count of Songs",
        title=f"Count of songs for selected artists",
        labels={"Artist Name": "Artist Name", "Count of Songs": "Count of Songs"},
    )
    fig_artist_count.update_layout(
        xaxis_title_text="", yaxis_title_text="Count of Songs"
    )

    return fig_artist_count


# Callback to update the top genres pie chart based on the radio button's value
@app.callback(
    Output("top-genres-pie-chart", "figure"), Input("genre-count-radio", "value")
)
def update_top_genres_pie_chart(selected_value):
    # Filter the genre counts based on the selected value
    top_genre_counts = genre_counts.head(selected_value)

    # Create the figure using Plotly Express for the top genres pie chart
    fig_top_genres_pie = px.pie(
        data_frame=top_genre_counts,
        names="Genre",
        values="Count",
        title=f"Pie Chart of Top {selected_value} Genres by Count",
    )

    return fig_top_genres_pie


if __name__ == "__main__":
    app.run_server(debug=True)
