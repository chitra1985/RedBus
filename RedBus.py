import streamlit as st
import pandas as pd
import numpy as np
import csv
import time
import pymysql
from cryptography.fernet import Fernet



myconnect = pymysql.connect(host = '0.0.0.0', port = 3306, user = 'root', passwd = 'MidhHeth@12', db='redbus')
cur = myconnect.cursor()
cur.execute("use redbus")


route_data = pd.read_csv("C:/Users/moort/GUVI-PROJECTS/RED_BUS/scraped_data.csv")
route_df = pd.DataFrame(data = route_data)



st.sidebar.image("C:/Users/moort/GUVI-PROJECTS/RED_BUS/rdc-redbus-logo.webp")

col_route, col_table = st.columns([1,3])

with col_route:
    state_dict ={'WBSTC': 'West Bengal', 'KSRTC':'Kerala', 'KAAC':'Assam', 'NBSTC':'North Bengal', 'KTCL':'Goa', 'JKSRTC':'Jammu & Kashmir', 'PEPSU':'Punjab', 'RSRTC':'Rajasthan'}
    #state_tuple = list(state_dict.items())
    state_df = pd.DataFrame(data = state_dict.values())
    #route_df['Category']
    

    state_sel = st.selectbox("Select State", options=state_df, index=0, placeholder="Choose State")
    state1 = [key for key, val in state_dict.items() if val == state_sel]
    
    route_df= route_df[route_df['Category']==state1[0]]
    

    if state_sel:

        route1 = st.selectbox("Select Route", options = route_df['Route Name'],index=1)
        column_head = ['BUS NAME', 'BUS TYPE', 'DEPARTING TIME', 'DURATION', 'REACHING TIME', 'FARE (INR)','SEATS AVAILABILITY']

        cur.execute("select BUSNAME,BUSTYPE,DEPARTING_TIME,DURATION,REACHING_TIME,PRICE,SEATS_AVAILABILITY from bus_routes where ROUTE_NAME = %s", (route1,))
        sql_bus = cur.fetchall()
        bus_df = pd.DataFrame(data = sql_bus, columns = column_head)

        type1 = st.selectbox("Select Bus Type:", options = bus_df['BUS TYPE'].unique(), placeholder="Slect type of bus")
        cur.execute("select BUSNAME,BUSTYPE,DEPARTING_TIME,DURATION,REACHING_TIME,PRICE,SEATS_AVAILABILITY from bus_routes where ROUTE_NAME = %s and BUSTYPE = %s", (route1,type1))
        sql_bus = cur.fetchall()
        bus_df = pd.DataFrame(data = sql_bus, columns = column_head)

        star = st.slider("Rating", min_value=1.0, max_value=5.0, step=0.5, value=5.0 )
        
        cur.execute("select BUSNAME,BUSTYPE,DEPARTING_TIME,DURATION,REACHING_TIME,PRICE,SEATS_AVAILABILITY from bus_routes where ROUTE_NAME = %s and BUSTYPE = %s and STAR_RATING <= %s", (route1,type1,star))
        sql_bus = cur.fetchall()
        bus_df = pd.DataFrame(data = sql_bus, columns = column_head)

        option = ['Below 500', '500 to 1000', ' Above 1000']    
        price = st.radio("Price Range", options = option, index=0)
        sel_opt = option.index(price)
        if price:
            if sel_opt == 0:
                cur.execute("select BUSNAME,BUSTYPE,DEPARTING_TIME,DURATION,REACHING_TIME,PRICE,SEATS_AVAILABILITY from bus_routes where ROUTE_NAME = %s and BUSTYPE = %s and STAR_RATING <= %s and PRICE < 500", (route1,type1,star))
                sql_bus = cur.fetchall()
                bus_df = pd.DataFrame(data = sql_bus, columns = column_head)
            elif sel_opt == 1:
                cur.execute("select BUSNAME,BUSTYPE,DEPARTING_TIME,DURATION,REACHING_TIME,PRICE,SEATS_AVAILABILITY from bus_routes where ROUTE_NAME = %s and BUSTYPE = %s and STAR_RATING <= %s and PRICE between 500 and 1000", (route1,type1,star))
                sql_bus = cur.fetchall()
                bus_df = pd.DataFrame(data = sql_bus, columns = column_head)
            elif sel_opt == 2:
                cur.execute("select BUSNAME,BUSTYPE,DEPARTING_TIME,DURATION,REACHING_TIME,PRICE,SEATS_AVAILABILITY from bus_routes where ROUTE_NAME = %s and BUSTYPE = %s and STAR_RATING <= %s and PRICE > 500", (route1,type1,star))
                sql_bus = cur.fetchall()
                bus_df = pd.DataFrame(data = sql_bus, columns = column_head)
    #sql_bus = cur.fetchall()
    

with col_table:
    if bus_df.shape[0] > 0:
        bus_df['hours'] = bus_df['DEPARTING TIME'].dt.components['hours']
        bus_df['mins'] = bus_df['DEPARTING TIME'].dt.components['minutes']
        bus_df['secs'] = bus_df['DEPARTING TIME'].dt.components['seconds']
        bus_df['DEPARTING TIME'] = bus_df['hours'].astype(str) + ":" + bus_df['mins'].astype(str) + ":" + bus_df['secs'].astype(str)
        bus_df = bus_df.drop(['hours','mins','secs'], axis=1)

        bus_df['hours'] = bus_df['REACHING TIME'].dt.components['hours']
        bus_df['mins'] = bus_df['REACHING TIME'].dt.components['minutes']
        bus_df['secs'] = bus_df['REACHING TIME'].dt.components['seconds']
        bus_df['REACHING TIME'] = bus_df['hours'].astype(str) + ":" + bus_df['mins'].astype(str) + ":" + bus_df['secs'].astype(str)
        bus_df = bus_df.drop(['hours','mins','secs'], axis=1)
    #bus_df['DEPARTING TIME'].dtypes
    if bus_df.shape[0] > 0:
        #st.write(bus_df.to_html(index=False), unsafe_allow_html= True)
        #st.dataframe(bus_df)
        st.write(bus_df.to_html(index=False), unsafe_allow_html= True)
    else:
        st.warning("No Buses Found")
    
st.sidebar.button("Home")
    

st.sidebar.button("Search Bus")




