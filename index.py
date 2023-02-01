from app import app, server
from routes import render_page_content
from layout.sidebar.sidebar_callbacks import toggle_collapse, toggle_classname
from pages.hyy.hyy_callbacks import update_figure
from pages.col.col_sonoro_callbacks import make_col_map
from pages.home.home_callbacks import make_col_map_home 
#from environment.settings import APP_HOST, APP_PORT, APP_DEBUG, DEV_TOOLS_PROPS_CHECK


if __name__ == "__main__":
    app.run_server(debug=True)