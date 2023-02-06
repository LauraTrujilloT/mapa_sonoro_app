from app import app, server
from routes import render_page_content
from layout.sidebar.sidebar_callbacks import toggle_collapse, toggle_classname
from pages.col.col_sonoro_callbacks import make_col_map
from pages.home.home_callbacks import make_col_map_home 


if __name__ == "__main__":
    app.run_server(debug=True)
    