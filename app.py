import dash
import dash_bootstrap_components as dbc
from flask_caching import Cache
from utils.external_assets import FONT_AWSOME
from layout.layout import layout
import flask


server = flask.Flask(__name__)

app = dash.Dash(
    __name__,
    title="Sound Map Dash App",
    server=server,
    suppress_callback_exceptions=True, 
    external_stylesheets=[
        dbc.themes.SPACELAB,
        FONT_AWSOME
    ],
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"}
    ]
)

cache = Cache(app.server, config={
    'CACHE_TYPE': 'filesystem',
    'CACHE_DIR': 'cache-directory'
})

app.layout = layout

server = app.server