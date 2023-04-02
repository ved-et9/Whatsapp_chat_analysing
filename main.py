import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import seaborn as sns
from collections import Counter
#sns.set()
from urlextract import URLExtract
extra=URLExtract()
def fetch_stat(user,data_f):
    if user== 'Overall':
        #no of meesages
        num_message=data_f.shape[0]
        #no of words
        words = []
        for message in data_f['message']:
            words.extend(message.split())
        #fetch number of media send

        no_of_media=data_f[data_f['message'] == '<Media omitted>\n'].shape[0]

        #fetch no of links
        links=[]
        for message in data_f['message']:
            links.extend(extra.find_urls(message))
        return num_message,len(words),no_of_media,len(links)



    else:

        #no of message
        new_data_f=data_f[data_f['user']== user]
        num_message=data_f[data_f['user'] == user].shape[0]


         #no of words
        words = []
        for message in new_data_f['message']:
            words.extend(message.split())
        #no_of_media
        no_of_media = new_data_f[new_data_f['message'] == '<Media omitted>\n'].shape[0]

        #no_of links
        links=[]
        for message in new_data_f['message']:
            links.extend(extra.find_urls(message))

        return num_message, len(words),no_of_media,len(links)


def most_busy_users(data_f):
    x = data_f['user'].value_counts().head()

    df=round((data_f['user'].value_counts() / data_f.shape[0]) * 100, 2).reset_index().rename(columns={'index': 'name', 'user': 'percentage'})
    return x,df


#wordcloud

def create_wordcloud(user,data_f):
    stop_word=[]
    with open("hinglish.txt", "r+") as f:
        lines = f.readlines()

        for line in lines:
            stop_word.append(line.replace("\n", ""))
    if user != 'Overall':
        data_f = data_f[data_f['user'] == user]
    temp = data_f[data_f['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    def remove_stop(message):
        q=[]
        for word in message.lower().split():
            if word not in stop_word:
                q.append(word)
        return " ".join(q)

    wcloud=WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    temp['message']=temp['message'].apply(remove_stop)
    df_wcloud=wcloud.generate((data_f['message'].str.cat(sep=" ")))
    return  df_wcloud

#most used words

def most_used_words(user,data_f):
    stop_word = []
    with open("hinglish.txt", "r+") as f:
        lines = f.readlines()

        for line in lines:
            stop_word.append(line.replace("\n", ""))
    if user != 'Overall':
        data_f = data_f[data_f['user'] == user]
    temp=data_f[data_f['user']!= 'group_notification']
    temp=temp[temp['message']!='<Media omitted>\n']


    words=[]
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_word:
                words.append(word)


    return pd.DataFrame(Counter(words).most_common(50))

#timeline
def monthly_timeline(user,data_f):
    if user != 'Overall':
        data_f = data_f[data_f['user'] == user]
    timeline = data_f.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))
    timeline['time'] = time
    return timeline
#dauily time line
def daily_timeline(user,data_f):
    if user != 'Overall':
        data_f = data_f[data_f['user'] == user]
    date_timeline = data_f.groupby('timeline_date').count()['message'].reset_index()
