from bs4 import BeautifulSoup
import pandas as pd
import streamlit as st
import investpy
import altair as alt
import datetime

st.title('FX tool')

st.sidebar.write("""
# 経済指標カレンダー
今週の経済指標カレンダー
""")

url = 'https://fx.minkabu.jp/indicators' #みんかぶFXの経済指標URLを取得
dfs = pd.read_html(url) #テーブルのオブジェクトを生成
dfs[0]

dfs1 = dfs[0].dropna(subset = [4]) #4番にNaNが入っている行はバグなので、削除
dfs2 = dfs1.drop(2,axis =1) #2番目の列を削除。axis = 1は列を削除するオプション
dfs2.columns = ["発表時間", "経済指標", "前回変動幅(USD/JPY)","前回","予想","結果"]#列名を手動で追加。

#前処理終了

dfs2

st.sidebar.table(dfs2)

st.title('経済指標グラフ')

economic_data = investpy.economic_calendar(time_zone=None, time_filter='time_only', countries=['japan', 'united states'], from_date='01/01/2021', to_date='11/06/2021')
ISM =economic_data[economic_data['event'].str.contains('ISM Non-Manufacturing PMI')]
date2 =[]
for i in ISM['date']:
    new_date = datetime.datetime.strptime(i,"%d/%m/%Y").strftime("%Y-%m-%d")
    date2.append(new_date)

ISM['date']=ISM['date'].str.replace('/','-')
ISM['date'] = date2
ISM.fillna(0)

chart =(
    alt.Chart(ISM)
    .mark_line(opacity=0.8,clip=True)
    .encode(
        x="date:T",
        y=alt.Y("actual:Q",stack=None)
    )
)
st.write(chart)