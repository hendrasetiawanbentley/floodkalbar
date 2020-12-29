
import dash
import dash_core_components as dcc


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

top_markdown_text = '''
This is my first deployed app
'''


if __name__ == '__main__':
    app.run_server(debug=True)
