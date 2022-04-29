from json.tool import main
import pandas as pd
import numpy as np
import re
import streamlit as st
import streamlit.components.v1 as stc
from htbuilder import HtmlElement, div, ul, li, br, hr, a, p, img, styles, classes, fonts
from htbuilder.units import percent, px
from htbuilder.funcs import rgba, rgb
import string
from pandas_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report




#html code
html_temp =  """
		<div style="background-color:#3872fb;padding:10px;border-radius:10px">
		<h1 style="color:white;text-align:center;">Toxilytics</h1>
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
    main_df['clean_message'] = main_df['message'].apply(lambda x: x.lower())
    #removing links
    main_df['clean_message'] = main_df['clean_message'].apply(lambda x: re.sub(r"http\S+", "", x))
    #removing digits 
    main_df['clean_message'] = main_df['clean_message'].apply(lambda x: re.sub('\w*\d\w*','', x))
    main_df['clean_message'] = main_df['clean_message'].apply(lambda x: re.sub('[%s]' % re.escape(string.punctuation), '', x))
    main_df['clean_message'] = main_df['clean_message'].apply(lambda x: remove_emoji(x))
    return main_df

def exists(x,y):
    if x in y:
        return 1
    else:
        return 0

def search(df,query):
    df['exists'] = df.apply(lambda x: exists(query,x['clean_message']),axis=1)
    outdf = df[df['exists'] == 1]
    outdf = outdf['user'].value_counts().reset_index()
    outdf.columns = ['user','counts']
    st.bar_chart(outdf)
    with st.container('Output'):
        st.dataframe(outdf)
        

def app():
    up_file = st.file_uploader('Upload Toxilytics generated data',type=['csv'])
    if up_file is not None:
        df = pd.read_csv(up_file)
        main_df = eda(df)
        st.dataframe(main_df)
        query = st.text_input('Search for the word')
        submit = st.button('Search')
        if submit:
            search(main_df,query)

    else:
        st.warning('Upload the toxilytics data')




def validate(df,name,email):
    try:
        if (len(df[(df['name'] == name)&(df['email'] == email)]) == 0):
            return 1
        return 0
    except Exception as ex:
        return 0


def signup():
    df = pd.read_csv('registered_users.csv')
    df = df.astype('str')
    new_user = st.sidebar.checkbox('Are you a new user?')
    rname = st.sidebar.text_input("Name")
    remail = st.sidebar.text_input("Email")
    rpasswd = st.sidebar.text_input("Password",type='password')
    rname = rname.lower()
    remail = remail.lower()
    st.session_state['rname'] = rname
    st.session_state['rpasswd'] = rpasswd
    st.session_state['remail'] = remail
    x = validate(df,rname,remail)
    
    if new_user:
        register = st.sidebar.checkbox('Register')
        if register:
            st.session_state['register'] = True
            l = {'name':rname,'email':remail,'password':rpasswd}
            df = df.append(l,ignore_index=True)
            df.to_csv('registered_users.csv',index=False)
            st.session_state['flag'] = True
            tbut = st.sidebar.button('Enter')
    else:
        login = st.sidebar.checkbox('Login')
        v1 = st.session_state['login']
        v2 = st.session_state['flag']
        
        if login:
            st.session_state['login'] = True
            if x == 0:
                d = list(df[(df['name'] == rname)&(df['email'] == remail)]['password'])
                if (d[0] != rpasswd):
                    st.sidebar.error('Password is incorrect')
                    st.stop()
                else:
                    st.session_state['flag'] = True
                    tbut = st.sidebar.button('Enter')
            else:
                st.sidebar.warning('Looks like you are a new user. Please select the checkbox for new user and register')
                st.stop()
             
            
                
            
            
  



  

if __name__ == '__main__':
  stc.html(html_temp)
  footer()

  if 'flag' not in st.session_state:
      st.session_state['flag'] = False
  if 'login' not in st.session_state:
      st.session_state['login'] = True
  if 'register' not in st.session_state:
      st.session_state['register'] = True
  if (st.session_state['login'] == True or st.session_state['register'] == True) and (st.session_state['flag'] == True):
      app()
  else:
      signup() 