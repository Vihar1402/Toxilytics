import pandas as pd
import os
import matplotlib.pyplot as plt
import string
import re
import math

def getFiles(path):
    fpaths = []
    for root,directories,files in os.walk(path):
        for f in files:
            fpaths.append(os.path.join(root,f))
    return fpaths

def getDirs(path):
    dpaths = []
    for root,directories,files in os.walk(path):
        for d in directories:
            dpaths.append(d)
    return dpaths

def getDf(path):
    fpaths = getFiles(path)
    li = []
    for f in fpaths:
        df = pd.read_csv(f)
        li.append(df)
    word_df = pd.concat(li,axis = 0, ignore_index=True)
    return word_df

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
    return outdf


