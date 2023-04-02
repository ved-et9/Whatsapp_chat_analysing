import matplotlib.pyplot as plt
import streamlit as st
import pre_process
import main

st.sidebar.title("Whatsap Chat Analyzer")
file=st.sidebar.file_uploader("choose a file")
if file is not None:
    by_data=file.getvalue()
    data=by_data.decode("utf-8")
    data_f=pre_process.pre_p(data)
    st.dataframe(data_f)

    users_list=data_f['user'].unique().tolist()
    #users_list.remove("90951")
    users_list.remove("812")
    users_list.remove("57078")
    users_list.remove("group_notification")
    users_list.sort()
    users_list.insert(0,"Overall")
    selected_user=st.sidebar.selectbox("Analysis w.r.t. user",users_list)


    if st.sidebar.button("Show Analysis"):
        number_of_messages,words,no_of_media,link_sent=main.fetch_stat(selected_user,data_f)
        col1,col2,col3,col4=st.columns(4)
        with col1:
            st.header("Total Messages")
            st.title(number_of_messages)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Media sent")
            st.title(no_of_media)
        with col4:
            st.header("Links Shared")
            st.title(link_sent)
        if selected_user == 'Overall':
            st.title('Most Busy Users')
            x,new_df=main.most_busy_users((data_f))
            fig, ax = plt.subplots()

            col1,col2=st.columns(2)

            with col1:
                ax.bar(x.index,x.values,color='yellow')

                st.pyplot(fig)

            with col2:

                st.dataframe(new_df)


            #word_cloud
        new_data = data_f[data_f['message'] != '<Media omitted>\n']
        df_wcloud=main.create_wordcloud(selected_user,new_data)
        fig,ax=plt.subplots()
        ax.imshow(df_wcloud)
        plt.grid(False)

        st.pyplot(fig)