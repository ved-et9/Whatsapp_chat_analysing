import streamlit as st
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import seaborn as sns
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
    if user != 'Overall':
        data_f=data_f[data_f['user'] == user]

    wcloud=WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    df_wcloud=wcloud.generate((data_f['message'].str.cat(sep=" ")))
    return  df_wcloud