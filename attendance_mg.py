import streamlit as st 
import pandas as pd 
import sqlite3 
from datetime import datetime, timedelta


conn = sqlite3.connect('data.db')
conn.execute('''
CREATE TABLE IF NOT EXISTS data ( 
name TEXT NOT NULL,
date TEXT NOT NULL, 
dep TEXT NOT NULL, 
start_time TEXT NOT NULL, 
finish_time TEXT NOT NULL 
)''')

st.header('勤怠管理') 
name = st.text_input("名前の入力")
dep = st.selectbox("部署の選択",(" ","営業","エンジニア", "スタッフ"))
date = st.date_input('日付を選択してください') 
start_time = st.time_input('出勤時間を選択してください') 
finish_time = st.time_input('退勤時間を選択してください')

if st.button('保存'): 
    date_str = date.strftime('%Y-%m-%d')  
    st_time_str = start_time.strftime('%H:%M:%S')
    fin_time_str = finish_time.strftime('%H:%M:%S') 
    if name != "":
        if dep != " ":
            conn.execute(f''' 
            INSERT INTO data (name, dep, date, start_time, finish_time)
            VALUES ('{name}','{dep}','{date_str}', '{st_time_str}', '{fin_time_str}')
            ''') 
            conn.commit()
        else:
            st.error("部署を選択してください")
    else:
        st.error("名前を入力してください")

df = pd.read_sql_query(f''' 
    SELECT name, dep, date, start_time, finish_time
    FROM data
''', conn)


st.table(df)
if st.button('データのリセット'): 
    conn.execute('DROP TABLE IF EXISTS data') 
    conn.execute(''' 
    CREATE TABLE ata ( 
    name TEXT NOT NULL, 
    dep TEXT NOT NULL, 
    date TEXT NOT NULL, 
    start_time TEXT NOT NULL, 
    finish_time TEXT NOT NULL 
    )''') 
    conn.commit() 
    st.success('データをリセットしました。')
