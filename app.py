import matplotlib.pyplot as plt
import streamlit as st
import pre_process
import main
import pandas as pd

st.sidebar.title("Whatsaap Chat Analyzer")
file=st.sidebar.file_uploader("choose a file")

if file is not None:

    by_data=file.getvalue()
    data=by_data.decode("utf-8")
    data_f=pre_process.pre_p(data)
    st.title("Your Data Frame")
    st.dataframe(data_f)

    users_list=data_f['user'].unique().tolist()

    users_list.remove("90951")
    users_list.remove("812")
    users_list.remove("57078")
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
        st.subheader("Timeline")
        timeline=main.monthly_timeline(selected_user,data_f)
        fig,ax =plt.subplots()
        ax.plot(timeline['time'], timeline['message'],color='orange')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
        #daily timeline

        date_timeline=main.daily_timeline(selected_user,data_f)
        plt.plot(date_timeline['timeline_date'], date_timeline['message'])
