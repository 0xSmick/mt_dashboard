#! /usr/bin/env python

# Example app

import os

import dash_core_components as dcc
import dash_html_components as html

from dash import Dash
from dash.dependencies import Input, Output
from flask import Flask, session

from dash_google_auth import GoogleOAuth
from flask_dance.contrib.google import google

# configure app
server = Flask(__name__)
app = Dash(
    __name__,
    server=server,
    url_base_pathname='/',
    auth='auth',
)
app.config['suppress_callback_exceptions']=True

# configure google oauth using environment variables
server.secret_key = os.environ.get("FLASK_SECRET_KEY", "supersekrit")

server.config["GOOGLE_OAUTH_CLIENT_ID"] = os.environ['GOOGLE_CLIENT_ID_MT']
server.config["GOOGLE_OAUTH_CLIENT_SECRET"] = os.environ['GOOGLE_SECRET_MT']

# allow for insecure transport for local testing (remove in prod)
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

# designate list of authorized emails
authorized_emails = [
    "lucas.chapin@gmail.com",
    "1234@example.com",
    "sheldonanalytics@gmail.com"
]

auth = GoogleOAuth(
    app,
    authorized_emails,
)

@server.route("/")
def MyDashApp():
    import pdb; pdb.set_trace();
    return app.index()

@server.route("/logout")
def logout():
    resp = google.post(
        'https://accounts.google.com/o/oauth2/revoke',
        params={'token': session['google_oauth_token']['access_token']},
        headers = {'content-type': 'application/x-www-form-urlencoded'}
    )
    session.clear()
    return '''
    <html>
        <head>
            <title>Logged Out</title>
        </head>
        <body>
            <h1>You have been logged out</h1>
        </body>
    </html>'''


app.layout = html.Div(children=[
    html.H1(children="Private Dash App"),
    html.A("Logout", href="http://localhost:8050/logout"),
    html.Div(id='placeholder', style={'display':'none'}),
    html.Div(id='welcome'),

    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                {'x': [1, 2, 3], 'y': [2, 4, 6], 'type': 'bar', 'name': 'Montreal'},
            ],
            'layout': {
                'title': 'Dash Data Visualization'
            }
        }
    )
])

@app.callback(
    Output('welcome', 'children'),
    [Input('placeholder', 'value')]
)
def on_load(value):
    return "Welcome, {}!".format(session['email'])

if __name__ == '__main__':
    app.run_server(host='localhost')
