import streamlit as st
import pandas as pd
from pytrends.request import TrendReq
import plotly.express as px

pytrend = TrendReq(hl = 'en-US', tz = 360)

st.title('Google Trends')

methode = st.selectbox('Methode', ('Nach Region', 'Top 10 nach Land', 'Interesse über Zeit'))

if methode == 'Nach Region':
    with st.form('1'):
        text = st.text_input('Suchbegriff')
        pytrend.build_payload(kw_list = [text])
        if st.form_submit_button('Auswerten'):
            st.subheader('Top 15')
            df = pytrend.interest_by_region()
            df = df.sort_values(by = [text], ascending = False)
            df2 = df.iloc[:15]
            fig = px.bar(df2, labels = {'geoName': 'Land', 'value': 'Polularität'})
            fig.update_layout(showlegend = False)
            fig.update_traces(marker_color = 'rgb(255,75,75)')
            st.plotly_chart(fig)
            st.subheader('Vollständige Ergebnisse')
            st.dataframe(df)

if methode == 'Top 10 nach Land':
    with st.form('1'):
        land = st.text_input('Land eingeben (kleinbuchstaben)')
        if st.form_submit_button('Auswerten'):
            df = pytrend.trending_searches(pn = land)
            st.subheader('Top 10')
            for i in range(10):
                st.write(str(i+1) + ' ' + df[0][i])
        

if methode == 'Interesse über Zeit':
    with st.form('1'):
        text = st.text_input('Suchbegriff(e)')
        jahre = st.slider('Zeitraum in Jahren', min_value = 1, max_value = 15, value = 5, step = 1)
        if ',' in text:
            text = text.split(',')
        else:
            text = [text]

        land = st.text_input('Ländercode eingeben (Großbuchsgaben)')
        if st.form_submit_button('Auswerten'):
            pytrend.build_payload(text, timeframe = str(2021-jahre) + '-01-01 2021-01-01', geo = land)
            df = pytrend.interest_over_time()
            fig = px.line(df, x = df.index, y = text, labels = {'date': 'Datum', 'value': 'Polularität'})
            st.plotly_chart(fig)

        
        


