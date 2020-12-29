import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import dash_daq as daq
import dash_table
from dash.exceptions import PreventUpdate

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

df = pd.read_csv('cleaneventdata.csv')
df.created_at = pd.to_datetime(df.created_at)
df.created_at = df.created_at.dt.date
banjir_count = df['created_at'].unique()
freq=len(banjir_count)
dfbnbp = pd.read_csv('Data Bencana_bnpb.csv')
dfbnbp['Tanggal Kejadian'] = pd.to_datetime(dfbnbp['Tanggal Kejadian'], format="%Y-%m-%d")
dfbnbp['Tanggal Kejadian']= dfbnbp['Tanggal Kejadian'].dt.date
banjir_count_BNPB = dfbnbp['Tanggal Kejadian'].unique()
freqbnpb=len(banjir_count_BNPB)
dfbnbp['Tanggal Kejadian'] = pd.to_datetime(dfbnbp['Tanggal Kejadian'], format="%Y-%m-%d")

tigathn = dfbnbp['Tanggal Kejadian'].groupby(dfbnbp['Tanggal Kejadian'].dt.to_period("M")).agg('count')
tigathn = pd.DataFrame(tigathn)
tigathn.columns = ['Jumlah Total Kejadian']
tigathn['Bulan Kejadian'] = tigathn.index
tigathn['Bulan Kejadian'] =tigathn['Bulan Kejadian'].apply(str)
tigathn['Bulan Kejadian'] =pd.to_datetime(tigathn['Bulan Kejadian'], format="%Y-%m")
tigathn['year'] = pd.DatetimeIndex(tigathn['Bulan Kejadian']).year
tigathn['year']=tigathn['year'].astype(str)
tigathn['month'] = pd.to_datetime(tigathn['Bulan Kejadian']).dt.strftime('%b')
#tigathn['Bulan kejadian']=tigathn.index
tigathn=tigathn.groupby(['month']).sum()
readytgntahun=pd.DataFrame(tigathn)
readytgntahun['bulan kejadian']=readytgntahun.index
readytgntahun=readytgntahun[['bulan kejadian','Jumlah Total Kejadian']]
readytgntahun=readytgntahun.sort_values(by='Jumlah Total Kejadian', ascending=False)
bulanbanjir = px.bar(readytgntahun,x='bulan kejadian',y='Jumlah Total Kejadian',color="bulan kejadian")
bulanbanjir.update_xaxes(type='category',tickmode='linear')

app.layout = html.Div([
    html.H2('Hello World'),
    dcc.Dropdown(
        id='dropdown',
        options=[{'label': i, 'value': i} for i in ['LA', 'NYC', 'MTL']],
        value='LA'
    ),
    html.Div(id='display-value')
])

@app.callback(dash.dependencies.Output('display-value', 'children'),
              [dash.dependencies.Input('dropdown', 'value')])
def display_value(value):
    return 'You have selected "{}"'.format(value)

if __name__ == '__main__':
    app.run_server(debug=True)
