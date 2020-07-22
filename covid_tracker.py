import pandas as pd
import plotly.figure_factory as pf
import numpy as np
import plotly.graph_objects as pg
from plotly.subplots import make_subplots
import plotly.express as px
import plotly.offline as py
from datetime import timedelta
import time

axis=dict(
    showline=False,
    zeroline=False,
    showgrid=False,
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
	yaxis1=dict(axis, **dict(domain=[0.7+0.02, 1.0], anchor='x1')),
	yaxis2=dict(axis, **dict(domain=[0.4+0.07, 0.7], anchor='x2')),
  yaxis3=dict(axis, **dict(domain=[0.2 + 0.02, 0.4+0.05], anchor='x3')),
  yaxis4=dict(axis, **dict(domain=[0.0, 0.2], anchor='x4'))
)

district = pd.read_csv('https://api.covid19india.org/csv/latest/district_wise.csv',index_col='SlNo',skiprows=[1])
state = pd.read_csv("https://api.covid19india.org/csv/latest/state_wise.csv",skiprows=[1])[['State','Confirmed','Recovered','Deaths','Active']]
daily = pd.read_csv('https://api.covid19india.org/csv/latest/state_wise_daily.csv')
district.drop(district.loc[district['State'] == 'State Unassigned'].index,inplace=True)
for i,x in enumerate(district['District']):
	if x == 'Unknown': district['District'].iloc[i] = district['State'].iloc[i]
daily['Date'] = daily['Date'].apply(lambda x: pd.to_datetime(x))
state_names={}
for x in district['State'].unique():
  state_names[x.lower()]=district['State_Code'].loc[district['State']==x].values[0]

def display_data(sentence):
  global district
  global state
  global daily
  global state_names
  date = daily['Date'].iloc[-1] - timedelta(days=30)
  dates = pd.date_range(start=date,end=daily['Date'].iloc[-1])
  col=''
  if 'full' in sentence:
    col = 'TT'
  else:
    for x in state_names:
      if x in sentence:
        col = state_names[x]
        print(col)
        break
    else:
      print("Couldn't find state")
      return 0
      
  confirmed = daily[col].loc[(daily['Date']>=date) & (daily['Status']=='Confirmed')].reset_index(drop=True)
  recovered = daily[col].loc[(daily['Date']>=date) & (daily['Status']=='Recovered')].reset_index(drop=True)
  deaths = daily[col].loc[(daily['Date']>=date) & (daily['Status']=='Deceased')].reset_index(drop=True)
  active = confirmed - recovered - deaths
  print("Collected data")
  if col=='TT':
    table_trace1 = pg.Table(header=dict(values=['States', 'Confirmed','Active','Deceased','Recovered']),
                 cells=dict(values=[state['State'], state['Confirmed'],state['Active'], state['Deaths'], state['Recovered']]),domain=dict(x=[0, 0.5],y=[0, 1.0]))
  else:
    district_values = district[['District','Confirmed','Active','Recovered','Deceased']].loc[district['State_Code']==col]
    district_values = district_values.sort_values(by=['Confirmed'],ascending=False)
    table_trace1 = pg.Table(header=dict(values=['Districts', 'Confirmed','Active','Deceased','Recovered']),
                 cells=dict(values=[district_values['District'], district_values['Confirmed'],district_values['Active'], district_values['Deceased'], district_values['Recovered']]),domain=dict(x=[0, 0.5],y=[0, 1.0]))
  trace1 = pg.Bar(x=dates,y=confirmed,name='Confirmed',marker={'color':'#FD073A'},xaxis='x1',yaxis='y1',textposition='auto',text=confirmed,texttemplate='%{text:.2s}',textangle=90)
  trace2 = pg.Bar(x=dates,y=active,name='Active',marker={'color':'#0080FF'},xaxis='x2',yaxis='y2',textposition='auto',text=active,texttemplate='%{text:.2s}',textangle=90)
  trace3 = pg.Bar(x=dates,y=recovered,name='Recovered',marker={'color':'#3ADF00'},xaxis='x3',yaxis='y3',textposition='auto',text=recovered,texttemplate='%{text:.2s}',textangle=90)
  trace4 = pg.Bar(x=dates,y=deaths,name='Deceased',xaxis='x4',yaxis='y4',textposition='auto',text=deaths,texttemplate='%{text:.2s}',textangle=90,marker={'color':'#FF8000'})
  print("Data visualization complete")
  fig1 = dict(data=[table_trace1, trace1, trace2, trace3, trace4], layout=layout1)
  py.plot(fig1)
