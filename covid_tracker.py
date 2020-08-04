import pandas as pd
import plotly.figure_factory as pf
import numpy as np
import plotly.graph_objects as pg
from plotly.subplots import make_subplots
import plotly.express as px
import plotly.offline as py
from datetime import timedelta
import time
import speech_recognition as sr
import os
from datetime import datetime

r = sr.Recognizer()
r.pause_threshold = 1

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

layout2 = dict(
	autosize=True,
	margin = dict(t=100),
	showlegend=True,
	xaxis1=dict(axis, **dict(domain=[0.55, 1], anchor='y1',showticklabels=False)),
	xaxis2=dict(axis, **dict(domain=[0.55, 1], anchor='y2')),
	yaxis1=dict(axis, **dict(domain=[0.5+0.02, 1.0], anchor='x1')),
	yaxis2=dict(axis, **dict(domain=[0, 0.4+0.07], anchor='x2'))
)

world = pd.read_csv('https://covid19.who.int/WHO-COVID-19-global-data.csv')
district = pd.read_csv('https://api.covid19india.org/csv/latest/district_wise.csv',index_col='SlNo',skiprows=[1])
state = pd.read_csv("https://api.covid19india.org/csv/latest/state_wise.csv")[['State','Confirmed','Recovered','Deaths','Active']]
daily = pd.read_csv('https://api.covid19india.org/csv/latest/state_wise_daily.csv')
district.drop(district.loc[district['State'] == 'State Unassigned'].index,inplace=True)
state.drop(state.loc[state['State'] == 'State Unassigned'].index,inplace=True)
for i,x in enumerate(district['District']):
	if x == 'Unknown': district['District'].iloc[i] = district['State'].iloc[i]
daily['Date'] = pd.to_datetime(daily['Date'])
world['Date_reported'] = pd.to_datetime(world['Date_reported'])
state_names={}
for x in district['State'].unique():
  state_names[x.lower()]=district['State_Code'].loc[district['State']==x].values[0]

def listen():
  with sr.Microphone() as source:
    os.system('clear')
    print("I'm Listening ......")
    r.adjust_for_ambient_noise(source, duration=1)
    audio = r.listen(source)
    try:
      print('Recognizing>')
      data = r.recognize_google(audio).lower()
      print(data)
    except:
      print("I don't Understand!")
      data = listen()
    return data

def display_district_data(col,state_name):
  last_updated = daily['Date'].iloc[-1].strftime("%d/%m/%Y")
  date = daily['Date'].iloc[-1] - timedelta(days=30)
  dates = pd.date_range(start=date,end=daily['Date'].iloc[-1])
  confirmed = daily[col].loc[(daily['Date']>=date) & (daily['Status']=='Confirmed')].reset_index(drop=True)
  recovered = daily[col].loc[(daily['Date']>=date) & (daily['Status']=='Recovered')].reset_index(drop=True)
  deaths = daily[col].loc[(daily['Date']>=date) & (daily['Status']=='Deceased')].reset_index(drop=True)
  active = confirmed - recovered - deaths
  print("Collected data")
  c,r,d,a = state.loc[state['State']==state_name].values.tolist()[0][1:]
    #c,r,d,a = str(c),str(r),str(d),str(a)
  district_values = district[['District','Confirmed','Active','Recovered','Deceased']].loc[district['State_Code']==col]
  district_values = district_values.sort_values(by=['Confirmed'],ascending=False)
  district_values = district_values[:-1]
  table_trace = pg.Table(header=dict(values=['<b>Districts</b>', '<b>Confirmed</b>','<b>Active</b>','<b>Recovered</b>','<b>Deceased</b>']),
                 cells=dict(values=[district_values['District'], district_values['Confirmed'],district_values['Active'],district_values['Recovered'],district_values['Deceased']]),domain=dict(x=[0, 0.5],y=[0, 0.9+0.05]))
  trace1 = pg.Scatter(x=dates,y=confirmed,name='Confirmed',marker={'color':'#FF8000'},xaxis='x1',yaxis='y1',text=confirmed,texttemplate='%{text:.2s}',fillcolor='#F7BE81',fill='tozeroy')
  trace2 = pg.Scatter(x=dates,y=active,name='Active',marker={'color':'#0080FF'},xaxis='x2',yaxis='y2',text=active,texttemplate='%{text:.2s}',fillcolor='#819FF7',fill='tozeroy')
  trace3 = pg.Scatter(x=dates,y=recovered,name='Recovered',marker={'color':'#3ADF00'},xaxis='x3',yaxis='y3',text=recovered,texttemplate='%{text:.2s}',fillcolor='#9FF781',fill='tozeroy')
  trace4 = pg.Scatter(x=dates,y=deaths,name='Deceased',xaxis='x4',yaxis='y4',text=deaths,texttemplate='%{text:.2s}',marker={'color':'#FD073A'},fillcolor='#F7819F',fill='tozeroy')
  print("Data visualization complete")
  layout1['title']='<b><i>Covid-19 Statistics</i></b>    Last updated:%s<br><br><b>Confirmed:</b>%d   <b>Active:</b>%d     <b>Recovered:</b>%d   <b>Deaths:</b>%d'%(last_updated,c,a,r,d)
  fig1 = dict(data=[table_trace, trace1, trace2, trace3, trace4], layout=layout1)
  py.plot(fig1)

def display_state_data(col):
  last_updated = daily['Date'].iloc[-1].strftime("%d/%m/%Y")
  date = daily['Date'].iloc[-1] - timedelta(days=30)
  dates = pd.date_range(start=date,end=daily['Date'].iloc[-1])
  confirmed = daily[col].loc[(daily['Date']>=date) & (daily['Status']=='Confirmed')].reset_index(drop=True)
  recovered = daily[col].loc[(daily['Date']>=date) & (daily['Status']=='Recovered')].reset_index(drop=True)
  deaths = daily[col].loc[(daily['Date']>=date) & (daily['Status']=='Deceased')].reset_index(drop=True)
  active = confirmed - recovered - deaths
  print("Collected data")
  c,r,d,a = list(state.iloc[0].values)[1:]
    #c,r,d,a = str(c),str(r),str(d),str(a)
  state.drop(0,inplace=True)
  table_trace = pg.Table(header=dict(values=['<b>States</b>', '<b>Confirmed</b>','<b>Active</b>','<b>Recovered</b>','<b>Deaceased</b>']),
                 cells=dict(values=[state['State'], state['Confirmed'],state['Active'],state['Recovered'],state['Deaths']]),domain=dict(x=[0, 0.5],y=[0, 0.9+0.05]))
  trace1 = pg.Scatter(x=dates,y=confirmed,name='Confirmed',marker={'color':'#FF8000'},xaxis='x1',yaxis='y1',text=confirmed,texttemplate='%{text:.2s}',fillcolor='#F7BE81',fill='tozeroy')
  trace2 = pg.Scatter(x=dates,y=active,name='Active',marker={'color':'#0080FF'},xaxis='x2',yaxis='y2',text=active,texttemplate='%{text:.2s}',fillcolor='#819FF7',fill='tozeroy')
  trace3 = pg.Scatter(x=dates,y=recovered,name='Recovered',marker={'color':'#3ADF00'},xaxis='x3',yaxis='y3',text=recovered,texttemplate='%{text:.2s}',fillcolor='#9FF781',fill='tozeroy')
  trace4 = pg.Scatter(x=dates,y=deaths,name='Deceased',xaxis='x4',yaxis='y4',text=deaths,texttemplate='%{text:.2s}',marker={'color':'#FD073A'},fillcolor='#F7819F',fill='tozeroy')
  print("Data visualization complete")
  layout1['title']='<b><i>Covid-19 Statistics</i></b>   Last updated:%s<br><br><b>Confirmed:</b>%d   <b>Active:</b>%d     <b>Recovered:</b>%d   <b>Deaths:</b>%d'%(last_updated,c,a,r,d)
  fig1 = dict(data=[table_trace, trace1, trace2, trace3, trace4], layout=layout1)
  py.plot(fig1)

def display_world_data():
  last_updated = world['Date_reported'].iloc[-1].strftime("%d/%m/%Y")
  date = world['Date_reported'].iloc[-1] - timedelta(days=30)
  dates = pd.date_range(start=date,end=daily['Date'].iloc[-1])
  confirmed,deaths = [],[]
  for x in dates:
    value = world[[' New_cases',' New_deaths']].loc[world['Date_reported']==x]
    confirmed.append(sum(value[' New_cases']))
    deaths.append(sum(value[' New_deaths']))
  c = sum(world[' Cumulative_cases'].loc[world['Date_reported']==world['Date_reported'].iloc[-1]].values)
  d = sum(world[' Cumulative_deaths'].loc[world['Date_reported']==world['Date_reported'].iloc[-1]].values)
  a = c-d
  current = world[[' Country',' Cumulative_cases',' Cumulative_deaths']].loc[world['Date_reported']==world['Date_reported'].iloc[-1]]
  current = current.sort_values(by=[' Cumulative_cases'],ascending=False)
  table_trace = pg.Table(header=dict(values=['<b>Country</b>', '<b>Confirmed</b>','<b>Active/Recovered</b>','<b>Deaceased</b>']),cells=dict(values=[current[' Country'], current[' Cumulative_cases'],current[' Cumulative_cases']-current[' Cumulative_deaths'],current[' Cumulative_deaths']]),
  domain=dict(x=[0, 0.5],y=[0, 0.9+0.05]))
  trace1 = pg.Scatter(x=dates,y=confirmed,name='Confirmed',marker={'color':'#FF8000'},xaxis='x1',yaxis='y1',text=confirmed,texttemplate='%{text:.2s}',fillcolor='#F7BE81',fill='tozeroy')
  trace2 = pg.Scatter(x=dates,y=deaths,name='Deceased',xaxis='x2',yaxis='y2',text=deaths,texttemplate='%{text:.2s}',marker={'color':'#FD073A'},fillcolor='#F7819F',fill='tozeroy')
  print("Data visualization complete")
  layout2['title']='<b><i>Covid-19 Statistics</i></b>   Last updated:%s<br><br><b>Confirmed:</b>%d   <b>Active/Recovered:</b>%d   <b>Deaths:</b>%d'%(last_updated,c,a,d)
  fig1 = dict(data=[table_trace, trace1, trace2], layout=layout2)
  py.plot(fig1)
  

"""def display_data(data):
  data = data.lower()
  col=''
  if 'world' in data:
    display_world_data()
  elif 'full' in data or 'india' in data:
    display_state_data('TT')
  else:
    for x in state_names:
      if x in data:
        col = state_names[x]
        state_name = x.upper().title()
        display_district_data(col,state_name)
        break
    else:
      print("Couldn't find state")
      return 0"""

if __name__ == "__main__":
    while True:
      data = listen()
      if 'goodbye' in data: break
      elif 'world' in data: display_world_data()
      elif 'full' in data or 'india' in data: display_state_data('TT')
      else:
        for x in state_names:
          if x in data:
            col = state_names[x]
            state_name = x.upper().title()
            display_district_data(col,state_name)
            break
        else:
          print("Couldn't find state")
      time.sleep(2)
      