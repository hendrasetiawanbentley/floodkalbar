import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

top_markdown_text = '''
This is my first deployed app
'''

df = pd.read_csv('dashboardready1.csv')
df = df.loc[df["Country Name"]!= "Equatorial Guinea"]
df = df.loc[df["Country Name"]!= "Argentina"]
df = df.loc[df["Country Name"]!= "Brazil"]
df = df.loc[df["Country Name"]!= "Bulgaria"]
df = df.loc[df["Country Name"]!= "Zimbabwe"]
df = df.loc[df["Country Name"]!= "Angola"]
df = df.loc[df["Country Name"]!= "Belarus"]
df = df.loc[df["Country Name"]!= "Tajikistan"]
df = df.loc[df["Country Name"]!= "Bahamas, The"]
df = df.loc[df["Country Name"]!= "Mongolia"]
df = df.loc[df["Country Name"]!= "Armenia"]
df = df.loc[df["Country Name"]!= "Uruguay"]
df = df.loc[df["Country Name"]!= "Romania"]
df = df.loc[df["Country Name"]!= "Bolivia"]
df = df.loc[df["Country Name"]!= "Trinidad and Tobago"]
df = df.loc[df["Country Name"]!= "Azerbaijan"]
df = df.loc[df["Country Name"]!= "Ukraine"]
df = df.loc[df["Country Name"]!= 'Kyrgyz Republic']
df = df.loc[df["Country Name"]!= 'Malawi']
df = df.loc[df["Country Name"]!= 'Madagascar']
df = df.loc[df["Country Name"]!= 'Colombia']
dftimeseries=df.loc[(df['Indicator Name']=='Real interest rate (%)') & (df['Value'].isna())]
x=dftimeseries["Country Name"]
available_indicators = df['Indicator Name'].unique()
dftimeseriesfinal = df[~df["Country Name"].isin(x)]
available_country=dftimeseriesfinal["Country Name"].unique()

import plotly.graph_objects as go 
dfs = px.data.gapminder().query("year==2007")
dffromwb = pd.read_csv('dashboardready1.csv')
dffromwb=dffromwb.rename(columns={"Country Name": "country"})
dffromwbbaddebt=dffromwb.loc[dffromwb['Indicator Name']=="Bank nonperforming loans to total gross loans (%)"]
dffromwbbankcredit=dffromwb.loc[dffromwb['Indicator Name']=="Domestic credit to private sector by banks (% of GDP)"]
dffromwbbaddebt=dffromwbbaddebt.fillna(0)
dffromwbbankcredit=dffromwbbankcredit.fillna(0)
dffromwbbaddebt=dffromwbbaddebt.rename(columns={"Value": "Bank nonperforming loans to total gross loans (%)"})
dffromwbbankcredit=dffromwbbankcredit.rename(columns={"Value": "Domestic credit to private sector by banks (% of GDP)"})
dfjoin = pd.merge(dfs, dffromwbbaddebt, on=['country'])

import quandl
# pandas for data manipulation
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.dates import MonthLocator, DateFormatter
quandl.ApiConfig.api_key = 'zNSVkNFKh_WNvSTkbvb9'
# Retrieve Morgan Stanly data from Quandl
morgan= quandl.get('WIKI/MS')
# Retrieve the Citigroup data from Quandl
gm = quandl.get('WIKI/C')



app.layout = html.Div([
    html.Div([
        html.Div([
            html.H1('Navigate through Turbulent Economic Period Using Banking Credit as a Fuel for the Economy', style={'textAlign': 'center'}),
            html.H4('(Cross Country and Past Economic Downturn Analysis)', style={'textAlign': 'center'}),
            ], style={'display': 'inline-block', 'width': '100%'}),
        html.P('In this pandemic, we should activate all of the resources that we have to get our economy back in a better position as soon as possible. Bank loans are very important tool because we know that, in the Covid19 pandemic, aggregate of demand is taking a hard hit. To fight this shock, Governments tend to lower their interest rate to help the economy. The scatter plot quadrants of real interest rate, Lending Interest rate and GPD annual growth show the movement to a lower level of interest rate during and after the economic downturn', className='my-class', id='my-p-element'),
    ], style={
        'borderBottom': 'thin lightgrey solid',
        'backgroundColor': 'rgb(250, 250, 250)',
        'padding': '10px 5px'
    }),
    
    
    html.Div([
        
        

        html.Div([
            dcc.Dropdown(
                id='crossfilter-xaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Real interest rate (%)'
            ),
            dcc.RadioItems(
                id='crossfilter-xaxis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ],
        style={'width': '49%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='crossfilter-yaxis-column',
                options=[{'label': 'GDP growth (annual %)', 'value': 'GDP growth (annual %)'}],
                value='GDP growth (annual %)'
            ),
            dcc.RadioItems(
                id='crossfilter-yaxis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ], style={'width': '49%', 'float': 'right', 'display': 'inline-block'})
    ], style={
        'borderBottom': 'thin lightgrey solid',
        'backgroundColor': 'rgb(250, 250, 250)',
        'padding': '10px 5px'
    }),

    html.Div([
        dcc.Graph(
            id='crossfilter-indicator-scatter',
            hoverData={'points': [{'customdata': 'Indonesia'}]}
        )
    ], style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'}),
   
    html.Div([ html.H4(' ') ], style={'display': 'inline-block', 'width': '2%'}),
    
    html.Div([
         html.H3('Real Interest Rate and GDP Annual Growth Scatter Plot Interpretation'),
         html.P('From this scatter plot in 1997, we know that most of the countries were hovering between 0% to 10% annual GDP growth and between 0% to 10% real interest rate.', className='v', id='v'),
         html.P('If you change the slider to 1998, the graph showed that many countries fell down to lower annual GDP growth. This means that countries with high annual GDP growth a year before experienced a downward pressure.', className='c', id='c'),
         html.P('In 1999 (year after economic downturn), we can notice that there is an increase in the number of countries with low real interest rate. This can be a sign that governments try to increase bank lending by lowering their interest rates.', className='f', id='f'),
         html.P('Similar trend is happening with Lending Interest Rates and in 2007 - 2008 Period', className='g', id='g'),
         html.Br(),
         html.Br(),
         html.Br(),
         ], style={'display': 'inline-block', 'width': '30%'}),
    
     html.Div(dcc.Slider(
        id='crossfilter-year--slider',
        min=df['Year'].min(),
        max=df['Year'].max(),
        value=df['Year'].max(),
        marks={str(year): str(year) for year in df['Year'].unique()},
        step=None
    ), style={'width': '49%', 'padding': '0px 20px 20px 20px'}),
     
     
    
    html.Div([
        
        html.Div([
            html.H4('Investigation to Individual Country Real Interest Rates and Lending Interest Rates Time Series Graph'),
            html.P('To give a solid evidence that countries in the world were trying to lower the rates as an effort to increase bank lending in the turbulent times, We can see from the time series variable below, that almost everytime GDP Annual Growth decline, lending interest rate and real interest rate is decline mostly in the year of crisis and one year after (Crisis Period 1997-1999 and 2007-2009. For most Asian Region, This is happening in 1997 - 1999 period and for most European, North America,South America and Mediterania Region, This trend happening in 2007 and 2009 period )')
        
        ], style={
        'borderBottom': 'thin lightgrey solid',
        'backgroundColor': 'rgb(250, 250, 250)',
        'padding': '10px 5px'
        }),
        html.Div([
             dcc.Dropdown(
                id='countryselection',
                options=[{'label': i, 'value': i} for i in available_country],
                value='Indonesia'
            ),
            dcc.Dropdown(options=[{'label': 'Real Interest Rates', 'value': 'Real interest rate (%)'},
                                        {'label': 'Lending Interest Rates', 'value': 'Lending interest rate (%)'}],
                               id='vartimeseriesx',
                               value='Real interest rate (%)'),
            
            ], style={'display': 'inline-block', 'width': '100%'}),
    
    ]),   
    html.Div([
        dcc.Graph(id='x-time-series')
    ], style={'width': '49%', 'display': 'inline-block'}), 
    html.Div([
          dcc.Graph(id='y-time-series')
         ], style={'display': 'inline-block', 'width': '49%'}),

   
      html.Div([
        html.H4('Banking Industry Itself'),
        html.P('Policy makers also need to maintain the banking industry itself to make sure that economic crisis not bring a financial system catastrophy'),
        html.P('Bank stock will signal a condition of banking industry. In the economic crisis period 1998 and 2008, We can see the decrease of bank\' stock value')
    ], style={'width': '100%', 'display': 'inline-block'}),
      
      dcc.Dropdown(id='ticker',options=[{'label': 'Morgan Stanley', 'value':1},
                                     {'label': 'Citigroup', 'value':'gm'}],
                            value='morgan'),
      
      dcc.Graph(id="time-series-chart"),
      html.P('We can see that the banking stock is taking a hit in two period of crisis 1997 - 1999 and 2007 - 2009. Therefore, Policy maker should keep and eye in the condition of the banking system while using it to help economic recovery. Goverment should focus in controling Bad Debt. I will show you the visualization of Bad Debt in time of crisis'),


    html.Div([
        html.H1('Banking Industry Bad Debt Heatmap', style={'textAlign': 'center'}),
        dcc.RadioItems(id='mapyear',
                       options=[
                           {'label': '2007', 'value': '2007'},
                           {'label': '2008', 'value': '2008'},
                           {'label': '2009', 'value': '2009'}
                           ],
                       value='2007',
                       labelStyle={'display': 'inline-block'}),  
        dcc.Graph(id="heatmap"),
        html.P('From the heat maps, we notice that bad debt was cool in 2007. Then when the downturn happened in 2008, the heat started to increase, and finally most of the country heat cooled down in 2009. This means that controlling the bad debt is also a part of the game plan when creating counter cyclical policy in an economic downturn.'),
        html.P('In conclusion, the Dashboard of  GDP growth (annual %), real interest rate (%), lending interest rate (%), and bank non-performing loans to total gross loans (%) shows that, historically, most of the developed country use Banking Credit to fight economic crisis, and This plan can utilize by developing country to fight the COVID19 economic crisis.')
    ],style={'width': '100%', 'float': 'right', 'display': 'inline-block'})


])

@app.callback(
    dash.dependencies.Output("heatmap", "figure"), 
    [dash.dependencies.Input("mapyear", "value")])

def display_map(mapyear):
    
    dfjoinyearselected=dfjoin.loc[dfjoin['Year']==int(mapyear)]

    fig = px.choropleth(dfjoinyearselected, locations="iso_alpha",
                    color="Bank nonperforming loans to total gross loans (%)", # lifeExp is a column of gapminder
                    hover_name="country", # column to add to hover information
                    color_continuous_scale=px.colors.sequential.OrRd)
    return fig            
                 
            
@app.callback(
    dash.dependencies.Output("time-series-chart", "figure"), 
    [dash.dependencies.Input("ticker", "value")])

def display_time_series(ticker):
    fig = px.line(morgan, x=morgan.index, y=morgan['Open'])
    if ticker=="gm":
        fig = px.line(gm, x=gm.index, y=gm['Open'])
    return fig

@app.callback(
    dash.dependencies.Output('crossfilter-indicator-scatter', 'figure'),
    [dash.dependencies.Input('crossfilter-xaxis-column', 'value'),
     dash.dependencies.Input('crossfilter-yaxis-column', 'value'),
     dash.dependencies.Input('crossfilter-xaxis-type', 'value'),
     dash.dependencies.Input('crossfilter-yaxis-type', 'value'),
     dash.dependencies.Input('crossfilter-year--slider', 'value')])

def update_graph(xaxis_column_name, yaxis_column_name,
                 xaxis_type, yaxis_type,
                 year_value):
    dff = df[df['Year'] == year_value]

    fig = px.scatter(x=dff[dff['Indicator Name'] == xaxis_column_name]['Value'],
            y=dff[dff['Indicator Name'] == yaxis_column_name]['Value'],
            hover_name=dff[dff['Indicator Name'] == yaxis_column_name]['Country Name']
            )

    fig.update_traces(customdata=dff[dff['Indicator Name'] == yaxis_column_name]['Country Name'])

    fig.update_xaxes(title=xaxis_column_name, type='linear' if xaxis_type == 'Linear' else 'log')

    fig.update_yaxes(title=yaxis_column_name, type='linear' if yaxis_type == 'Linear' else 'log')

    fig.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, hovermode='closest')

    return fig


def create_time_series(dff, axis_type, title):

    fig = px.scatter(dff, x='Year', y='Value')

    fig.update_traces(mode='lines+markers')

    fig.update_xaxes(showgrid=False)

    fig.update_yaxes(type='linear' if axis_type == 'Linear' else 'log')

    fig.add_annotation(x=0, y=0.85, xanchor='left', yanchor='bottom',
                       xref='paper', yref='paper', showarrow=False, align='left',
                       bgcolor='rgba(255, 255, 255, 0.5)', text=title)

    fig.update_layout(height=225, margin={'l': 20, 'b': 30, 'r': 10, 't': 10})

    return fig


@app.callback(
    dash.dependencies.Output('x-time-series', 'figure'),
    [dash.dependencies.Input('countryselection', 'value'),
     dash.dependencies.Input('vartimeseriesx', 'value'),
     dash.dependencies.Input('vartimeseriesx', 'value')
     ])

def update_x_timeseries(hoverData, yaxis_column_name, axis_type):
    country_name = hoverData
    dff = df[df['Country Name'] == country_name]
    dff = dff[dff['Indicator Name'] == yaxis_column_name]
    axis_type='Linear'
    title = '<b>{}</b><br>{}'.format(country_name, yaxis_column_name)
    return create_time_series(dff, axis_type, title)




@app.callback(
    dash.dependencies.Output('y-time-series', 'figure'),
    [dash.dependencies.Input('countryselection', 'value'),
     dash.dependencies.Input('crossfilter-yaxis-column', 'value')
     ])

def update_y_timeseries(hoverData, xaxis_column_name):
    country_name = hoverData
    dff = df[df['Country Name'] == country_name]
    dff = dff[dff['Indicator Name'] == 'GDP growth (annual %)']
    axis_type='Linear'
    title = '<b>{}</b><br>{}'.format(country_name, xaxis_column_name)
    return create_time_series(dff, axis_type, title)

if __name__ == '__main__':
    app.run_server(debug=True)
