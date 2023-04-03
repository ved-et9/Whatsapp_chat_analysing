# Whatsapp_chat_analysing

## This is a web app which can be used to analyse  whatsapp group chat.
You can analyze different parameters like the most busy users,most common words used , days on which the group is more active,the time period in day which has more activeness.
These parameters can be analyzed for overall or on any specific participants
.The analysis is shown as different graphs and dataframes


** points to remember

* It works for data when your time setting is on 24 hour clock to overcome this situation either use 24 hour clock or change regex equation in pre_process file
  to way = '\d{1,2}/\d{1,2}/\d{1,2},\s\d{1,2}:\d{2}\s\w{2}\s-\s'
* To run the app type <-streamlit run app.py-> in terminal