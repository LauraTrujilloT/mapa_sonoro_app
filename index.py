from app import app, server
from routes import render_page_content
from layout.sidebar.sidebar_callbacks import toggle_collapse, toggle_classname
from pages.gdp.gdp_callbacks import update_figure
from pages.iris.iris_callbacks import make_graph
from pages.hyy.hyy_callbacks import update_figure
#from environment.settings import APP_HOST, APP_PORT, APP_DEBUG, DEV_TOOLS_PROPS_CHECK


if __name__ == "__main__":
    app.run_server(debug=True)