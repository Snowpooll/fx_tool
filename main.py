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
#dfs[0]

dfs1 = dfs[0].dropna(subset = [4]) #4番にNaNが入っている行はバグなので、削除
dfs2 = dfs1.drop(2,axis =1) #2番目の列を削除。axis = 1は列を削除するオプション
dfs2.columns = ["発表時間", "経済指標", "前回変動幅(USD/JPY)","前回","予想","結果"]#列名を手動で追加。

#前処理終了

dfs2

st.sidebar.table(dfs2)

st.title('経済指標グラフ')

#ISM チャート

economic_data = investpy.economic_calendar(time_zone=None, time_filter='time_only', countries=['japan', 'united states'], from_date='01/01/2021', to_date='11/06/2021')
ISM =economic_data[economic_data['event'].str.contains('ISM Non-Manufacturing PMI')]
date2 =[]
for i in ISM['date']:
    new_date = datetime.datetime.strptime(i,"%d/%m/%Y").strftime("%Y-%m-%d")
    date2.append(new_date)

ISM['date']=ISM['date'].str.replace('/','-')
ISM['date'] = date2
ISM.fillna(0)

# chart =(
#     alt.Chart(ISM)
#     .mark_line(opacity=0.8,clip=True)
#     .encode(
#         x="date:T",
#         y=alt.Y("actual:Q",stack=None)
#     )
# )
st.markdown("### ISM チャート")
# st.write(chart)

actual =(
    alt.Chart(ISM)
    .mark_line(opacity=0.8,clip=True)
    .encode(
        x="date:T",
        y=alt.Y("actual:Q",stack=None)
    )
)

forecast =(
    alt.Chart(ISM)
    .mark_line(opacity=0.8,clip=True,color='red')
    .encode(
        x="date:T",
        y=alt.Y("forecast:Q",stack=None),       
    )
)

previous =(
    alt.Chart(ISM)
    .mark_line(opacity=0.8,clip=True,color='green')
    .encode(
        x="date:T",
        y=alt.Y("previous:Q",stack=None),       
    )
)
st.markdown("### 前回までのグラフ　青＝結果、赤＝予測値")
st.markdown("### 今回の数値")

current_score = 69
st.write(current_score)
st.markdown("### 前回の数値と差分")
previous_score2 =pd.to_numeric(ISM['actual'],errors="coerce")
sabun_score = current_score - previous_score2.at[previous_score2.index[-1]]
st.write("今回の差分は",sabun_score)
#st.write(previous_score2.tail(1))

ism_score = ISM.at[ISM.index[-1],'actual']
st.write("前回の数値は",ism_score,"でした")
st.write("前回の数値は",previous_score2.at[previous_score2.index[-1]],"でした")

st.write(alt.layer(actual,forecast).resolve_scale(
    y = 'independent'
))

st.write("金価格")

gold =investpy.commodities.get_commodity_historical_data(commodity="Gold", from_date='01/01/2021', to_date='01/09/2021', country=None, as_json=False, order='ascending', interval='Daily')
gold.reset_index()
gold.index = gold.index.strftime('%Y/%m/%d')
gold= gold.T
gold= gold.T.reset_index()
gold_chart =(
    alt.Chart(gold)
    .mark_line(opacity=0.8,clip=True)
    .encode(
        x="Date:T",
        y=alt.Y("Close:Q",stack=None)
    )
)
st.write(gold.tail(1))
st.write(gold_chart)

st.write("WTI価格")
wti = investpy.get_commodity_recent_data(commodity='Crude Oil WTI')
wti.reset_index()
wti.index = wti.index.strftime('%Y/%m/%d')
wti= wti.T
wti= wti.T.reset_index()

st.write(wti.tail(1))
oil_chart =(
    alt.Chart(wti)
    .mark_line(opacity=0.8,clip=True)
    .encode(
        x="Date:T",
        y=alt.Y("Close:Q",stack=None)
    )
)
st.write(oil_chart)