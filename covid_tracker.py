import pandas as pd
import plotly.figure_factory as pf
import numpy as np
import plotly.graph_objects as pg
from plotly.subplots import make_subplots
import plotly.express as px
import plotly.offline as py

district = pd.read_csv('https://api.covid19india.org/csv/latest/district_wise.csv',index_col='SlNo')
state = pd.read_csv("https://api.covid19india.org/csv/latest/state_wise.csv",skiprows=[1])[['State','Confirmed','Recovered','Deaths','Active']]
daily = pd.read_csv('https://api.covid19india.org/csv/latest/state_wise_daily.csv')
district.drop(district.loc[district['State'] == 'State Unassigned'].index,inplace=True)
for i,x in enumerate(district['District']):
	if x == 'Unknown': district['District'].iloc[i] = district['State'].iloc[i]

values = np.array(district['District'])
Confirmed = np.array(district['Confirmed'])
deaths = np.array(district['Deceased'])
active = np.array(district['Active'])
recovered = np.array(district['Recovered'])

table_trace1 = pg.Table(header=dict(values=['Districts', 'Confirmed','Active','Deceased','Recovered']),
                 cells=dict(values=[values, Confirmed, active, deaths, recovered]),domain=dict(x=[0, 0.5],y=[0, 1.0]))
trace1 = pg.Bar(x=values,y=Confirmed,name='Confirmed',marker={'color':'#FA5882'},xaxis='x1',yaxis='y1')
trace2 = pg.Bar(x=values,y=active,name='Active',marker={'color':'#01DF01'},xaxis='x2',yaxis='y2')
trace3 = pg.Bar(x=values,y=recovered,name='Recovered',marker={'color':'#2E9AFE'},xaxis='x3',yaxis='y3')
trace4 = pg.Bar(x=values,y=deaths,name='Deceased',xaxis='x4',yaxis='y4')

axis=dict(
    showline=True,
    zeroline=False,
    showgrid=True,
    mirror=True,
    ticklen=5,
    gridcolor='#ffffff',
    tickfont=dict(size=10)
)

layout1 = dict(
	autosize=True,
	title='Covid-19 Statistics',
	margin = dict(t=100),
	showlegend=True,
	xaxis1=dict(axis, **dict(domain=[0.55, 1], anchor='y1',showticklabels=False)),
	xaxis2=dict(axis, **dict(domain=[0.55, 1], anchor='y2',showticklabels=False)),
	xaxis3=dict(axis, **dict(domain=[0.55, 1], anchor='y3',showticklabels=False)),
	xaxis4=dict(axis, **dict(domain=[0.55, 1], anchor='y4')),
	yaxis1=dict(axis, **dict(domain=[0.7, 1.0], anchor='x1')),
	yaxis2=dict(axis, **dict(domain=[0.4+0.07, 0.7], anchor='x2')),
  yaxis3=dict(axis, **dict(domain=[0.2 + 0.02, 0.4+0.05], anchor='x3')),
  yaxis4=dict(axis, **dict(domain=[0.0, 0.2], anchor='x4'))
)

fig1 = dict(data=[table_trace1, trace1, trace2, trace3, trace4], layout=layout1)
py.plot(fig1)