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
tigathn['Bulan kejadian']=tigathn.index
tigathn=tigathn.groupby(['month']).sum()
readytgntahun=pd.DataFrame(tigathn)
readytgntahun['bulan kejadian']=readytgntahun.index
readytgntahun=readytgntahun[['bulan kejadian','Jumlah Total Kejadian']]
readytgntahun=readytgntahun.sort_values(by='Jumlah Total Kejadian', ascending=False)
#bulanbanjir = px.bar(readytgntahun,x='bulan kejadian',y='Jumlah Total Kejadian',color="bulan kejadian")
#bulanbanjir.update_xaxes(type='category',tickmode='linear')

precipitation = pd.read_csv('pontianak.csv')
precipitation['date_time'] = pd.to_datetime(precipitation['date_time'], format="%Y-%m-%d")
precipitation['month'] = pd.to_datetime(precipitation['date_time']).dt.strftime('%b')
precipitationbulanan = precipitation.groupby(['month'])['precipMM'].mean()
precipitationbulanan=pd.DataFrame(precipitationbulanan)
precipitationbulanan['bulan']=precipitationbulanan.index
precipitationbulanan=precipitationbulanan[['bulan','precipMM']]
precipitationbulanan=precipitationbulanan.sort_values(by='precipMM', ascending=False)
curfig  = px.bar(precipitationbulanan,x='bulan',y='precipMM',color="bulan")
curfig.update_xaxes(type='category',tickmode='linear')
curfig.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)')


app.layout = html.Div([
    html.Div(
        children=[
                    html.Div([
                     html.Div([html.H1('Analisa Efek Banjir dan Mitigasi Resiko Pada Dunia Bisnis Kalimantan Barat', style={'textAlign': 'center','background': '#f9f9f9','box-shadow': '0 0 1px rgba(0,0,0,.2), 0 2px 4px rgba(0,0,0,.1)','border-radius': '5px','margin-bottom': '20px','text-shadow': '1px 1px 1px rgba(0,0,0,.1)'})]),
                             
                        
                    html.H2('Dashboard Berdasarkan Data BNPB', style={'textAlign': 'center','borderBottom': 'thin lightgrey solid',
        'backgroundColor': 'rgb(250, 250, 250)',
        'padding': '10px 5px'}),
                    ]),
                    
                    html.Div([
                    html.Div([
                        html.H5("Grafik Total Kejadian Banjir Berdasarkan Tahun: "),
                                 dcc.Dropdown(options=[{'label': '2017', 'value':'2017'},
                                                    {'label': '2018', 'value':'2018'},
                                                    {'label': '2019', 'value':'2019'},
                                                    {'label': '2020', 'value':'2020'},
                                    ],
                        id='tahun-multidropdown',
                           multi=True,
                           value=['2017','2018','2019','2020']),
                        html.H5("Grafik Total Kejadian Banjir Berdasarkan Kabupaten: "),   
                            dcc.Dropdown(options=[{'label': 'BENGKAYANG', 'value':'BENGKAYANG'},
                                                    {'label': 'KAPUAS HULU', 'value':'KAPUAS HULU'},
                                                    {'label': 'KAYONG UTARA', 'value':'KAYONG UTARA'},
                                                    {'label': 'KETAPANG', 'value':'KETAPANG'},
                                                    {'label': 'KOTA SINGKAWANG', 'value':'KOTA SINGKAWANG'},
                                                    {'label': 'KUBU RAYA', 'value':'KUBU RAYA'},
                                                    {'label': 'LANDAK', 'value':'LANDAK'},
                                                    {'label': 'MELAWI', 'value':'MELAWI'},
                                                    {'label': 'MEMPAWAH', 'value':'MEMPAWAH'},
                                                    {'label': 'SAMBAS', 'value':'SAMBAS'},
                                                    {'label': 'SANGGAU', 'value':'SANGGAU'},
                                                    {'label': 'SEKADAU', 'value':'SEKADAU'},
                                                    {'label': 'SINTANG', 'value':'SINTANG'},
                                    ],
                        id='kabupaten-multidropdown',
                           multi=True,
                           value=['BENGKAYANG','KAPUAS HULU','KAYONG UTARA','KETAPANG','KOTA SINGKAWANG','KUBU RAYA','LANDAK','MELAWI','MEMPAWAH','SAMBAS','SANGGAU','SEKADAU','SINTANG']),
                         html.H5("Grafik Total Kejadian Banjir", style={'textAlign': 'center'}),
                            dcc.Graph(id='eventhistogram')],
                        style={'width': '70%', 'display': 'inline-block','background': '#f9f9f9','box-shadow': '0 0 1px rgba(0,0,0,.2), 0 2px 4px rgba(0,0,0,.1)','border-radius': '5px','margin-bottom': '20px','text-shadow': '1px 1px 1px rgba(0,0,0,.1)'}),
                      html.Div([
                          html.P("Tabel Bulanan Total Kejadian Periode 2017 - 2020"),
                          dcc.Dropdown(options=[{'label': 'Seluruh Kalimantan Barat', 'value':'all'},
                                                {'label': 'BENGKAYANG', 'value':'BENGKAYANG'},
                                                    {'label': 'KAPUAS HULU', 'value':'KAPUAS HULU'},
                                                    {'label': 'KAYONG UTARA', 'value':'KAYONG UTARA'},
                                                    {'label': 'KETAPANG', 'value':'KETAPANG'},
                                                    {'label': 'KOTA SINGKAWANG', 'value':'KOTA SINGKAWANG'},
                                                    {'label': 'KUBU RAYA', 'value':'KUBU RAYA'},
                                                    {'label': 'LANDAK', 'value':'LANDAK'},
                                                    {'label': 'MELAWI', 'value':'MELAWI'},
                                                    {'label': 'MEMPAWAH', 'value':'MEMPAWAH'},
                                                    {'label': 'SAMBAS', 'value':'SAMBAS'},
                                                    {'label': 'SANGGAU', 'value':'SANGGAU'},
                                                    {'label': 'SEKADAU', 'value':'SEKADAU'},
                                                    {'label': 'SINTANG', 'value':'SINTANG'},],
                           id='3tahunanlokasi',
                           value='all'),
                          dash_table.DataTable(
                              id='memory-table',
                              columns=[{'name': i, 'id': i} for i in readytgntahun.columns],
                              data=readytgntahun.to_dict('records')
                              ),
                          
                          
                          ],style={'width': '28%', 'display': 'inline-block','float': 'right','background': '#f9f9f9','box-shadow': '0 0 1px rgba(0,0,0,.2), 0 2px 4px rgba(0,0,0,.1)','border-radius': '5px','margin-bottom': '20px','text-shadow': '1px 1px 1px rgba(0,0,0,.1)'})
            
                  ],
              style={'width': '100%', 'display': 'inline-block', 'float': 'right'}),
            html.Div([
                html.Div([
                    html.H5("Data Weather Station Average Precipitation/Curah Hujan periode 2015 - 2020 "),
                    dcc.Graph(figure=curfig),
                    html.P("Terjadi pergeseran seasonal tiap tahun", style={'textAlign': 'center'}),
                    
                    ],style={'width': '50%', 'display': 'inline-block'}),
                html.Div([
                    html.H5("Data Bulanan Banjir Periode 2017 - 2020"),
                    dcc.Dropdown(options=[{'label': 'Seluruh Kalimantan Barat', 'value':'all'},
                                                {'label': 'BENGKAYANG', 'value':'BENGKAYANG'},
                                                    {'label': 'KAPUAS HULU', 'value':'KAPUAS HULU'},
                                                    {'label': 'KAYONG UTARA', 'value':'KAYONG UTARA'},
                                                    {'label': 'KETAPANG', 'value':'KETAPANG'},
                                                    {'label': 'KOTA SINGKAWANG', 'value':'KOTA SINGKAWANG'},
                                                    {'label': 'KUBU RAYA', 'value':'KUBU RAYA'},
                                                    {'label': 'LANDAK', 'value':'LANDAK'},
                                                    {'label': 'MELAWI', 'value':'MELAWI'},
                                                    {'label': 'MEMPAWAH', 'value':'MEMPAWAH'},
                                                    {'label': 'SAMBAS', 'value':'SAMBAS'},
                                                    {'label': 'SANGGAU', 'value':'SANGGAU'},
                                                    {'label': 'SEKADAU', 'value':'SEKADAU'},
                                                    {'label': 'SINTANG', 'value':'SINTANG'},],
                           id='3tahunanlokasigraph',
                           value='all'),
                    dcc.Graph(id='graptotalperbandingan'),
                    html.P("Ketinggian permukaan pasang mempengaruhi event banjir", style={'textAlign': 'center'})
                    
                    
                    
                    ],style={'width': '50%', 'display': 'inline-block'}),
                ],style={'width': '100%', 'display': 'inline-block', 'float': 'right','background': '#f9f9f9','box-shadow': '0 0 1px rgba(0,0,0,.2), 0 2px 4px rgba(0,0,0,.1)','border-radius': '5px','margin-bottom': '20px','text-shadow': '1px 1px 1px rgba(0,0,0,.1)'}),
             html.Div(
                        children=[
                            dcc.Store(id='memory-output'),
                           
  
                            html.Div([
                            html.P("Kejadian Banjir di Kalimantan Barat Data Twitter Periode Februari 2017, 15 - Desember 2020, 6",style={'width': '45%'}),
                            daq.LEDDisplay(
                                id="tweet-led",
                                value=freq,
                                color="#92e0d3",
                                backgroundColor="#1e2130",
                                )],style={'width': '50%', 'display': 'inline-block', 'padding': '0 20','align':'center'}),
                            
                            
                            html.Div([
                            html.P("Kejadian Banjir di Kalimantan Barat Data BNPB Periode Februari 2017, 15 - Desember 2020, 6",style={'width': '45%'}),
                            daq.LEDDisplay(
                                id="bnpb-led",
                                value=freqbnpb,
                                color="#92e0d3",
                                backgroundColor="#1e2130"
                                )],style={'width': '50%', 'display': 'inline-block', 'padding': '0 20'})
                            
                            
                        ],style={'width': '100%' ,'display': 'inline-block','border':'3px solid #fff'}
                        
                        
                        
                        ),
            html.Div([
                html.H3("Interpretasi Data Pada Dunia Bisnis", style={'textAlign': 'center','background': '#f9f9f9','box-shadow': '0 0 1px rgba(0,0,0,.2), 0 2px 4px rgba(0,0,0,.1)','border-radius': '5px','margin-bottom': '20px','text-shadow': '1px 1px 1px rgba(0,0,0,.1)'}),
                html.P(" Dunia usaha di Kalimantan Barat dipastikan akan mengalami kerugian di saat terjadi banjir, namun signifikasi dampak tersebut akan berbeda untuk tiap sektor. Sektor Retail, Pertanian, Konstruksi dan Perbankan akan terdampak cukup signifikan dikarenakan model bisnis yang terhubung dengan konektifitas transportasi dan keadaan cuaca.", style={'textAlign': 'left','borderBottom': 'thin lightgrey solid'}),
                html.Div([
                html.Div([
                html.H6("Sektor Retail", style={'textAlign': 'center','borderBottom': 'thin lightgrey solid'}),
                html.P(" - Menurut Bappenas pemberian likuiditas kepada UKM yang terdampak banjir untuk memulai lagi dan mempertahankan operasional bisnis sangat penting. Selain itu penerapan manajemen resiko yang baik akan dapat mengurangi magnitude dampak kerugian bisnis. Pengusaha dan Pihak terkait yang dapat menyediakan likuiditas tambahan dapat melakukan persiapan dengan mengalokasikan liquiditas cadangan pada bulan yang memiliki resiko banjir tinggi di Kalimantan Barat.", style={'textAlign': 'left'}),
                html.P(" - Sebagai contoh dalam 3 tahun terakhir, Bulan November, Januari, Juli, September, dan Desember kejadian banjir di Provinsi Kalimantan Barat cukup tinggi. Oleh karena itu,  UKM dan Perusahaan yang bergerak di sektor retail dapat mempersiapkan cadangan likuiditas  pada bulan - bulan berisiko banjir tersebut untuk menjaga cashflow dan operasional perusahaan", style={'textAlign': 'left'}),
                ],style={'width': '48%', 'display': 'inline-block', 'float':'left','background': '#f9f9f9','box-shadow': '0 0 1px rgba(0,0,0,.2), 0 2px 4px rgba(0,0,0,.1)','border-radius': '5px','margin-bottom': '20px','text-shadow': '1px 1px 1px rgba(0,0,0,.1)'}),
                html.Div([
                html.H6("Sektor Konstruksi dan Proyek Pemerintah", style={'textAlign': 'center','borderBottom': 'thin lightgrey solid'}),
                html.P(" - Untuk sektor konstruksi, berdasarkan penelitian Findy Kamaruzzaman, Penyebab terlambat nya pengerjaan penyelesaian proyek konstruksi adalah kenaikan harga bahan peringkat 2, kelangkaan material peringkat 3, dan pengaruh cuaca pada pengerjaan peringkat 4.", style={'textAlign': 'left'}),
                html.P(" - Namun untuk untuk disadari, Banjir dan Curah hujan yang tinggi memiliki hubungan causal yang dapat menyebabkan kenaikan bahan baku, kelangkaan material dan menghambat day to day operation dari pengerjaan konstruksi.", style={'textAlign': 'left'}),
                html.P(" - Dalam rangka memitigasi resiko - resiko tersebut, Kontraktor dan Pemilik Pekerjaan dapat memperhitungkan analisa curah hujan dan kemungkinan banjir pada pengerjaan proyek yang melewati bulan dengan curah hujan tinggi sebagai contoh dalam 3 tahun terakhir (Februari, Januari dan Maret) dan (November, Januari, Juli, September, dan Desember).", style={'textAlign': 'left'}),
                html.P(" - Intensitas Curah hujan akan bergeser dan dipengaruhi cuaca. Apabila terjadi pergeseran, Persiapan terhadap kemungkinan curah hujan tinggi  tidak akan menjadi cost yang terbuang sia - sia karna dapat dimanfaatkan pada saat terjadi pergeseran", style={'textAlign': 'left'}),
                html.P(" - Sebagai contoh, Pemesanan dan Pengiriman bahan dapat dilaksanakan secara massive sebelum bulan berisiko curah hujan tinggi, untuk menghidari kelangkaan, kesulitan pengirimanan dan penyimpanan dan kenaikan harga", style={'textAlign': 'left'}),
                html.P(" - Perancangan dan pelaksanaan pekerjaan  proyek harus dapat memperhitungkan bulan - bulan dengan resiko curah hujan dan banjir yang tinggi. Pemantauan ketinggian pasang air juga menjadi faktor yang dipantau dikarenakan banjir juga dipengaruhi oleh hal tersebut", style={'textAlign': 'left'}),
                html.P(" - Penerapan Asuransi, pemantauan Lebih Sering pada Bulan berisiko, quality control, hedging bahan baku, dan perancangan metode addendum pada saat risk event terjadi adalah hal - hal yang harus dilakukan agar dapat melakukan pengerjaan proyek yang optimal", style={'textAlign': 'left'}),
                ],style={'width': '48%', 'display': 'inline-block', 'float': 'right','background': '#f9f9f9','box-shadow': '0 0 1px rgba(0,0,0,.2), 0 2px 4px rgba(0,0,0,.1)','border-radius': '5px','margin-bottom': '20px','text-shadow': '1px 1px 1px rgba(0,0,0,.1)'}),
                ],style={'width': '100%', 'display': 'inline-block', 'float': 'right'}),
                html.Div([
                html.Div([
                html.H6("Sektor Pertanian", style={'textAlign': 'center','borderBottom': 'thin lightgrey solid'}),
                html.P(" - Secara umum sektor pertanian memiliki exposure resiko serupa dengan sektor kontruksi dan proyek pemerintah. Siklus tanam dan panen harus memperhitungkan resiko banjir dan curah hujan yang tinggi", style={'textAlign': 'left'}),
                html.P(" - Asuransi usaha tani yang digagas oleh industri jasa keuangan dan didukung pemerintah dapat menjadi alat dalam melakukan mitigasi resiko", style={'textAlign': 'left'}),
                html.P(" - Berdasarkan UNDANG-UNDANG REPUBLIK INDONESIA NOMOR 19 TAHUN 2013 TENTANG PERLINDUNGAN DAN PEMBERDAYAAN PETANI, Asuransi Pertanian adalah perjanjian antara Petani dan pihak perusahaan asuransi untuk mengikatkan diri dalam pertanggungan risiko Usaha Tani   ", style={'textAlign': 'left'}),
                ],style={'width': '48%', 'display': 'inline-block', 'float': 'left','background': '#f9f9f9','box-shadow': '0 0 1px rgba(0,0,0,.2), 0 2px 4px rgba(0,0,0,.1)','border-radius': '5px','margin-bottom': '20px','text-shadow': '1px 1px 1px rgba(0,0,0,.1)'}),
                html.Div([
                html.H6("Sektor Perbankan", style={'textAlign': 'center','borderBottom': 'thin lightgrey solid'}),
                html.P(" - Resiko yang dihadapi perbankan adalah resiko lanjutan yang dihadapi oleh setiap sektor sesuai dengan kredit yang diberikan pada sektor tersebut", style={'textAlign': 'left'}),
                html.P(" - Untuk debitur sektor retail, Perbankan dapat melakukan analisa pro forma terhadap cashflow debitur untuk menghadapi bulan bulan yang berisiko. Selain itu, untuk beberapa jenis kredit yang memiliki collateral berupa inventory ataupun aset bangunan, Bank dapat melalukan pengecekan, re-evaluasi, dan analisa apakah collateral tersebut akan terdampak curah hujan dan event banjir pada bulan bulan berisiko", style={'textAlign': 'left'}),
                html.P(" - Untuk debitur sektor konstruksi proyek dan konstruksi pada proyek - proyek pemerintah, Perbankan dapat memasukan resiko curah hujan tinggi dan banjir apabila pengerjaan melewati bulan bulan berisiko. Dikarenakan pekerjaan yang progress nya terhambat dapat mempengaruhi termin pembayaran. Selain itu  resiko tersebut dapat menjadi risk premium yang mempengaruhi struktur harga kredit yang ditawarkan oleh perbankan kepada debitur dan menjadi salah satu unsur covenant dan perjanjian kredit", style={'textAlign': 'left'}),
                html.P(" - Untuk debitur sektor pertanian, Perbankan dapat melakukan mitigasi resiko untuk memantau apakah debitur telah memperhitungkan siklus curah hujan dan banjir dalam siklus bercocok tanam. Hasil analisa tersebut adalah risk premium dan dapat membuat klausa - klausa khusus yang dapat melindungi debitur dan memastikan kesuksesan kredit yang diberikan", style={'textAlign': 'left'}),
                ],style={'width': '48%', 'display': 'inline-block', 'float': 'right','background': '#f9f9f9','box-shadow': '0 0 1px rgba(0,0,0,.2), 0 2px 4px rgba(0,0,0,.1)','border-radius': '5px','margin-bottom': '20px','text-shadow': '1px 1px 1px rgba(0,0,0,.1)'}),
                ]),
                ],style={'width': '100%', 'display': 'inline-block', 'float': 'right'}),
             html.Div([
                html.H6("Disclaimer", style={'textAlign': 'center','background': '#f9f9f9','box-shadow': '0 0 1px rgba(0,0,0,.2), 0 2px 4px rgba(0,0,0,.1)','border-radius': '5px','margin-bottom': '20px','text-shadow': '1px 1px 1px rgba(0,0,0,.1)'}),
                html.P("Segala rekomendasi dan analisa hanyalah bersifat memberi pandangan semata, dan Virya Data Scientia tidak bertanggung jawab atas keuntungan atau kerugian yang timbul, kami melarang untuk mengambil keputusan apapun berdasarkan analisa dan rekomendasi pada dashboard ini.", style={'textAlign': 'left','font-size': '8px'}),
                html.P("Data banjir bersumber dari website BNPB (https://gis.bnpb.go.id/) di akses tanggal 06 Desember 2020", style={'textAlign': 'left','font-size': '8px'}),
                html.P("Data weather station bersumber dari  https://www.worldweatheronline.com/developer/api/historical-weather-api.aspx di akses tanggal 06 Desember 2020", style={'textAlign': 'left','font-size': '8px'}),
                html.P("Data Bappenas bersumber dari Laporan Perkiraan Kerusakan dan Kerugian Pasca Bencana Banjir Awal Februari 2007 di Wilayah Jabodetabek ", style={'textAlign': 'left','font-size': '8px'}),
                html.P("Data Penilitian Proyek bersumber dari Studi Keterlambatan Penyelesaian Proyek Konstruksi oleh Findy Kamaruzzaman", style={'textAlign': 'left','font-size': '8px'}),
                html.P("Virya Data Scientia tidak menjamin semua informasi yang disajikan akurat dan lengkap sehingga Virya Data Scientia tidak bertanggung jawab atas segala kesalahan dan keterlambatan memperbarui informasi, dan melarang keputusan atau tindakan yang diambil berdasarkan penggunaan informasi yang ada pada dashboard ini", style={'textAlign': 'left','font-size': '8px'}),
                html.P("Dashboard ini hanya ditujukan untuk kepentingan edukasi dan bukan rekomendasi untuk untuk melakukan aktivitas yang terkait dengan kegiatan apapun.", style={'textAlign': 'left','font-size': '8px'}),
                 ]) ,
             html.Div([
                
                 ]) 
                        
                      
                        
                    
    ])
  ],style={'background-color:': 'center'})
        
@app.callback(
    dash.dependencies.Output('eventhistogram','figure'),
    [dash.dependencies.Input('tahun-multidropdown','value'),
     dash.dependencies.Input('kabupaten-multidropdown','value')]
    )
       
# Update the histogram

def update_hist(name,kabupaten):
    dfbnbp = pd.read_csv('Data Bencana_bnpb.csv')
    dfbnbp =   dfbnbp [  dfbnbp ['Kabupaten'].isin(kabupaten)]
    dfbnbp['Tanggal Kejadian'] = pd.to_datetime(dfbnbp['Tanggal Kejadian'], format="%Y-%m-%d")
    dfbnbp['Tanggal Kejadian']= dfbnbp['Tanggal Kejadian'].dt.date
    banjir_count_BNPB = dfbnbp['Tanggal Kejadian'].unique()
    freqbnpb=len(banjir_count_BNPB)
    dfbnbp['Tanggal Kejadian'] = pd.to_datetime(dfbnbp['Tanggal Kejadian'], format="%Y-%m-%d")
    #create selection for the dataset
    #untuk histogram feed to the graph
    freq_kej=dfbnbp['Tanggal Kejadian'].groupby(dfbnbp['Tanggal Kejadian'].dt.to_period("M")).agg('count')
    freq_kej=pd.DataFrame(freq_kej)
    freq_kej.columns = ['Jumlah Total Kejadian']
    freq_kej['Bulan Kejadian'] = freq_kej.index
    freq_kej['Bulan Kejadian'] =freq_kej['Bulan Kejadian'].apply(str)
    freq_kej['Bulan Kejadian'] =pd.to_datetime(freq_kej['Bulan Kejadian'], format="%Y-%m")
    freq_kej['year'] = pd.DatetimeIndex(freq_kej['Bulan Kejadian']).year
    freq_kej['month'] = pd.to_datetime(freq_kej['Bulan Kejadian']).dt.strftime('%b')
    freq_kej['year']=freq_kej['year'].astype(str)
    freq_kej['Bulan Kejadian'] = freq_kej[['year', 'month']].apply(lambda x: '-'.join(x), axis=1)
    df = freq_kej
    df =  df [ df ['year'].isin(name)]
    newfig  = px.bar(df,x='Bulan Kejadian',y='Jumlah Total Kejadian',color="Jumlah Total Kejadian",color_continuous_scale='reds')
    newfig.update_xaxes(type='category',tickmode='linear')
    newfig.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)')
    return newfig 

@app.callback(dash.dependencies.Output('graptotalperbandingan', 'figure'),
              dash.dependencies.Input('3tahunanlokasigraph', 'value'))
def filter_lks(lks):
    if lks=='all':
        # Return all the rows on initial load/no country selected.
        dfbnbp = pd.read_csv('Data Bencana_bnpb.csv')
        dfbnbp['Tanggal Kejadian'] = pd.to_datetime(dfbnbp['Tanggal Kejadian'], format="%Y-%m-%d")
        #create selection for the dataset
        #untuk histogram feed to the graph
        #jumlah banjir bulanan kalimantan barat
        #untuk menampilkan tabel
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
        bulanbanjir.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)')
        return bulanbanjir

    #create selection for the dataset
    #untuk histogram feed to the graph
    #jumlah banjir bulanan kalimantan barat
    #untuk menampilkan tabel
    dfbnbp = pd.read_csv('Data Bencana_bnpb.csv')
    dfbnbp=dfbnbp.loc[(dfbnbp['Kabupaten']==lks)]
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
    bulanbanjir.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)')
    return bulanbanjir


if __name__ == '__main__':
    app.run_server(debug=True)
