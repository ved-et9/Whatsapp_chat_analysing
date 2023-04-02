import matplotlib.pyplot as plt
import streamlit as st
import pre_process
import main
import pandas as pd
from matplotlib.pyplot import figure
import seaborn as sns

st.sidebar.title("Whatsaap Chat Analyzer")
file=st.sidebar.file_uploader("choose a file")

if file is not None:

    by_data=file.getvalue()
    data=by_data.decode("utf-8")
    data_f=pre_process.pre_p(data)
    st.title("Your Data Frame")
    st.dataframe(data_f)

    users_list=data_f['user'].unique().tolist()

    #users_list.remove("90951")
    #users_list.remove("812")
    #users_list.remove("57078")
    users_list.remove("group_notification")
    users_list.sort()
    users_list.insert(0,"Overall")
    selected_user=st.sidebar.selectbox("Analysis w.r.t. user",users_list)

    st.title("Statistical Analysis")
    if st.sidebar.button("Show Analysis"):
        number_of_messages,words,no_of_media,link_sent=main.fetch_stat(selected_user,data_f)
        col1,col2,col3,col4=st.columns(4)
        with col1:
            st.subheader("Total Messages")
            st.header(number_of_messages)
        with col3:
            st.subheader("Total Words")
            st.header(words)
        with col2:
            st.subheader("Media sent")
            st.header(no_of_media)
        with col4:
            st.subheader("Links Shared")
            st.header(link_sent)
        if selected_user == 'Overall':
            st.subheader('Most Busy Users')

            x,new_df=main.most_busy_users((data_f))
            fig, ax = plt.subplots()

            col1,col2=st.columns(2)

            with col1:

                ax.bar(x.index,x.values,color='yellow')

                st.pyplot(fig)

            with col2:
                st.subheader("Most Contribution")
                st.dataframe(new_df)


            #word_cloud
        st.subheader("Word cloud")
        new_data = data_f[data_f['message'] != '<Media omitted>\n']
        df_wcloud=main.create_wordcloud(selected_user,new_data)
        fig,ax=plt.subplots()
        ax.imshow(df_wcloud)
        plt.grid(False)

        st.pyplot(fig)




        #most used words
        col1,col2=st.columns(2)
        with col1:
            st.subheader("Most used words")
            most_data_f=main.most_used_words(selected_user,data_f)

            st.dataframe(most_data_f)



        #timeline
        st.subheader("Monthly Timeline")
        timeline=main.monthly_timeline(selected_user,data_f)
        fig,ax =plt.subplots()
        ax.stem(timeline['time'], timeline['message'])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
        #daily timeline
        st.subheader("Daily Timeline")
        date_timeline=main.daily_timeline(selected_user,data_f)
        fig, ax = plt.subplots()
        plt.plot(date_timeline['timeline_date'], date_timeline['message'])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
         #activity map
        st.subheader("Activity Map")
        col1,col2=st.columns(2)

        with col1:
            st.subheader("Most busy Day")
            busy_day = main.weekly_act(selected_user,data_f)
            fig,ax=plt.subplots()

            plt.xticks(rotation='vertical')
            ax.bar(busy_day.index,busy_day.values)
            st.pyplot(fig)
        with col2:
            st.subheader("Most busy Month")
            busy_month = main.month_activity(selected_user, data_f)
            fig, ax = plt.subplots()
            plt.xticks(rotation='vertical')
            ax.bar(busy_month.index, busy_month.values,color='green')
            st.pyplot(fig)



        #busiest and quitest day
        col1,col2=st.columns(2)
        bu,qu=main.busy_quiet(selected_user,data_f)
        with col1:
            st.subheader("Busiest day's")
            st.dataframe(bu)
        with col2:
            st.subheader("Quitiest day's")
            st.dataframe(qu)
        st.text("Here <index> is the  day no. from starting day of the group and for person analysis ")
        st.text("it is from their joining date")


        #heat_map
        st.subheader("Day Long Heat Map")
        heat_map_u=main.heat_map(selected_user,data_f)
        fig,ax=plt.subplots()

        ax=sns.heatmap(heat_map_u)
        st.pyplot(fig)