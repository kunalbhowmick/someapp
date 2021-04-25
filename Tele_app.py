# -*- coding: utf-8 -*-
"""
Created on Mon Apr 19 18:40:40 2021

@author: k.bhowmick
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import plotly.express as px
import random

st.sidebar.title('Tele-App')

with st.beta_expander("MTD Volume Metrics"):
    c1,c2,c3,c4=st.beta_columns(4)
    
    with c1:
        if st.button('Metric1'):
            import random
            result=random.randint(50,100)
            st.write('MTD TR: %s' % result)
       
    with c2:
        if st.button('Metric2'):
            import random
            result=random.randint(50,100)
            st.write('MTD CRD: %s' % result)
            
    with c3:
        if st.button('Metric3'):
            import random
            result=random.randint(40,80)
            st.write('MTD Completion: %s' % result)
            
    with c4:
        if st.button('Something_else'):
            import random
            result=random.randint(40,100)
            st.write('MTD Something_else: %s' % result)
        
############################################### Date range #################################        

with st.sidebar.beta_expander("Date Filters"):       
    import streamlit as st
    import time
    import datetime
    from datetime import datetime, date, time
    col1,col2 = st.beta_columns(2)
    
    with col1:   
       start = st.date_input('Start date')
       
       
    with col2:
        End = st.date_input('End date')
###########################################
import requests
import io

url = "https://raw.githubusercontent.com/kunalbhowmick/streamlit-forecast/main/input.csv" # Make sure the url is the raw version of the file on GitHub

#url='https://raw.githubusercontent.com/kunalbhowmick/someapp/main/input.csv'
download = requests.get(url).content


df=pd.read_csv(io.StringIO(download.decode('utf-8')),header=0,date_parser='Month')

# Filter the data 
with st.sidebar.beta_expander("DATA Filters"):
    Forecast_Category=st.selectbox('Select Forecast Category:', df['FC'].unique() )
    df_filter=df[(df['FC']==Forecast_Category)]
    
    Division=st.selectbox('Select Division:', df_filter['Division'].unique() )
    df_filter=df_filter[(df_filter['Division']==Division)]
    
    Region=st.selectbox('Select Region:', df_filter['Region'].unique() )
    df_filter=df_filter[(df_filter['Region']==Region)]
    
    District=st.selectbox('Select District:', df_filter['District'].unique() )
    df_filter=df_filter[(df_filter['District']==District)]


#Chart

#fig = px.line(df_filter, x="Month", y="Volume" ,color='Type',title=str(Forecast_Category)+str(Division)+str(Region)+str(District))
              
#st.write(fig)

###################################### Adjusted line for the forecast #########################

df_adjusted=df_filter.copy()

df_adjusted_actual=df_adjusted[(df_adjusted['Type']=='Actuals')]

df_adjusted_forecast=df_adjusted[(df_adjusted['Type']=='Forecast 8+4')].append(df_adjusted[(df_adjusted['Type']=='Forecast 9+3')])


################# Forecast Adjust Factor#####################
with st.sidebar.beta_expander("Forecast Adjust Factor"):
    CHOICES = {0.8: "- 20%", 0.9: "- 10%", 1: "no change",1.1: "+ 10%",1.2: "+ 20%"}
    
    
    def format_func(option):
        return CHOICES[option] 
    
    option = st.selectbox("Forecast Adjust Factor", options=list(CHOICES.keys()), format_func=format_func)
 
df_adjusted_forecast['Adjusted_Volume'] = df['Volume'].apply(lambda x: x*option)

###########################################################################################
import plotly.graph_objects as go

# Create traces
fig = go.Figure()
fig.add_trace(go.Scatter(x=df_adjusted_actual['Month'], y=df_adjusted_actual['Volume'],
                    mode='lines',
                    name='Actual'))
fig.add_trace(go.Scatter(x=df_adjusted_forecast['Month'], y=df_adjusted_forecast['Volume'],
                    mode='lines+markers',
                    name='Forecast'))
fig.add_trace(go.Scatter(x=df_adjusted_forecast['Month'], y=df_adjusted_forecast['Adjusted_Volume'],
                    mode='lines+markers', name='Adjusted_Forecast'))
st.write(fig)

# Table
df_table=df_filter.copy()
df_table=df_table[['Month','Type','Volume']]


with st.beta_expander("Forecast Version"):
#st.table(pd.pivot_table(df_table,index=['Type'],columns=['Month']))
    st.dataframe(pd.pivot_table(df_table,index=['Type'],columns=['Month']))
    #st.markdown(get_table_download_link(df_table), unsafe_allow_html=True)


