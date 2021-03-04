"""
Dashboard_Sentiment_Anlysis

Created by Giovanni E. Bonaventura

"""

import base64
import datetime
import io
import plotly.express as px
import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from plotly_wordcloud import plotly_wordcloud as pwc
import re
import pandas as pd


def tweets_list(tweets):
    nonPunct = re.compile('.*[A-Za-z].*')  # must contain a letter or digit
    text =''
    for list_words_tweets in tweets: 
        for w in list_words_tweets.split(' '):
            if nonPunct.match(w):
                text+=w+' '
    return text

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        # Allow multiple files to be uploaded
        multiple=True
    ),
    html.Div(id='Pie-chart'),
])


def parse_contents(contents, filename, list_of_dates):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')), names=['text','class'], header=1)
    except Exception as e:
        print(e)
    fig = px.pie(df, values=df['class'].value_counts(), names=df['class'].value_counts().index)
    fig.update_layout(transition_duration=500)
    text=tweets_list(list(df['text'].values))
    return html.Div([
        html.Div([
        html.H5(filename),

        dash_table.DataTable(
            data=df.to_dict('records'),
            columns=[{'name': i, 'id': i} for i in df.columns],
            style_table={
            'height': 300,
            'overflowY': 'scroll'
        }
        ),

        html.Hr(),  # horizontal line

        ]),
        html.Div([dcc.Graph( figure=fig)]),
        html.Div([dcc.Graph( figure=pwc(text))])
        ])

@app.callback(Output('Pie-chart', 'children'),
              [Input('upload-data', 'contents')],
              [State('upload-data', 'filename'),
               State('upload-data', 'last_modified')])
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in zip(list_of_contents, list_of_names, list_of_dates)]
        return children
        



if __name__ == '__main__':
    app.run_server(debug=True)
