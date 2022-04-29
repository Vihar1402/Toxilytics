#!/usr/bin/python
# -*- coding: utf-8 -*-
from json.tool import main
import pandas as pd
import numpy as np
import os
import re
import streamlit as st
import streamlit.components.v1 as stc
from htbuilder import HtmlElement, div, ul, li, br, hr, a, p, img, styles, classes, fonts
from htbuilder.units import percent, px
from htbuilder.funcs import rgba, rgb
from datetime import date
from stqdm import stqdm
stqdm.pandas()
import string




inp_path = 'data/'

# html code

html_temp = """
		<div style="background-color:#3872fb;padding:10px;border-radius:10px">
		<h1 style="color:white;text-align:center;"> Toxilytics </h1>
		</div>
		"""

def footer():
    myargs = [
        "Maintained by Vihar\n",
        "- Version 1.0"]
    layout(*myargs)

def layout(*args):

    style = """
    <style>
      # MainMenu {visibility: hidden;}
      footer {visibility: hidden;}
     .stApp { bottom: 105px; }
    </style>
    """

    style_div = styles(
        position="fixed",
        left=0,
        bottom=0,
        margin=px(0, 0, 0, 0),
        width=percent(100),
        color="red",
        text_align="center",
        height="auto",
        opacity=1
    )

    style_hr = styles(
        display="block",
        margin=px(8, 8, "auto", "auto"),
        border_style="inset",
        border_width=px(2)
    )

    body = p()
    foot = div(
        style=style_div
    )(
        hr(
            style=style_hr
        ),
        body
    )

    st.markdown(style, unsafe_allow_html=True)

    for arg in args:
        if isinstance(arg, str):
            body(arg)

        elif isinstance(arg, HtmlElement):
            body(arg)

    st.markdown(str(foot), unsafe_allow_html=True)


def get_dirs(path):
    dirs = []
    for it in os.scandir(path):
        if it.is_dir():
            if it.name != '.ipynb_checkpoints':
                 dirs.append(it.name)
    return dirs


def get_df(path):
    df = pd.DataFrame()
    for f in os.listdir(path):
        
        fpath = os.path.join(path,f)
        
        temp = pd.read_csv(fpath)
        df = df.append(temp)
    
    return df
    
#removing emojis
def remove_emoji(string):
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002500-\U00002BEF"  # chinese char
                               u"\U00002702-\U000027B0"
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               u"\U0001f926-\U0001f937"
                               u"\U00010000-\U0010ffff"
                               u"\u2640-\u2642"
                               u"\u2600-\u2B55"
                               u"\u200d"
                               u"\u23cf"
                               u"\u23e9"
                               u"\u231a"
                               u"\ufe0f"  # dingbats
                               u"\u3030"
                               "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', string)

def eda(main_df):
    #lowercasing message
    dtp = {'message': str}
    main_df = main_df.astype(dtp)
    main_df['clean_message'] = main_df['message'].progress_apply(lambda x: x.lower())
    #removing links
    main_df['clean_message'] = main_df['clean_message'].progress_apply(lambda x: re.sub(r"http\S+", "", x))
    #removing digits 
    main_df['clean_message'] = main_df['clean_message'].progress_apply(lambda x: re.sub('\w*\d\w*','', x))
    main_df['clean_message'] = main_df['clean_message'].apply(lambda x: re.sub('[%s]' % re.escape(string.punctuation), '', x))
    main_df['clean_message'] = main_df['clean_message'].apply(lambda x: remove_emoji(x))
    return main_df




def app():
    servers = get_dirs(inp_path)
    server = st.selectbox('Choose Your Server', servers)
    path = inp_path + server
    channels = get_dirs(path)
    channel = st.selectbox('Choose Your channel', channels)
    analyse = st.checkbox('Analyse')
    if analyse:
        fin_path = inp_path + server + '/' + channel
        df = get_df(fin_path)
        print(df.dtypes)
        fin_df = eda(df)
        st.dataframe(fin_df)



        




def login():

  passwd = st.sidebar.text_input("Password",type = "password")
  login = st.sidebar.button("Login")
  st.session_state['login'] = True
  st.session_state['passwd'] = passwd
  if login:
    if passwd != "admin":
      st.sidebar.error("Password is incorrect")




if __name__ == "__main__":
    st.set_page_config(layout='wide')
    stc.html(html_temp)

    footer()
    if 'login' not in st.session_state:
        st.session_state['login'] = True
    if 'passwd' not in st.session_state:
        st.session_state['passwd'] = ''
    if st.session_state['login'] == True and st.session_state['passwd'] == 'admin':
        app()
    else:
        login()





 	

    
    


        	



