import re
import pandas as pd


def pre_p(data):
    way = '\d{1,2}/\d{1,2}/\d{1,2},\s\d{1,2}:\d{2}\s-\s'
    message = re.split(way, data)[1:]

    dates = re.findall(way, data)

    data_f = pd.DataFrame({'user_message': message, 'message_dates': dates})
    data_f['message_dates'] = pd.to_datetime(data_f['message_dates'], format='%m/%d/%y, %H:%M - ')

    data_f.rename(columns={'message_dates': 'date'}, inplace=True)
    users = []
    messages = []
    for message in data_f['user_message']:
        entry = re.split('([\w]+?):\s', message)
        if entry[1:]:  # user_name
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])
    data_f['user'] = users
    data_f['message'] = messages
    data_f.drop(columns=['user_message'], inplace=True)

    data_f['year'] = data_f['date'].dt.year
    data_f['month'] = data_f['date'].dt.month_name()
    data_f['day'] = data_f['date'].dt.day
    data_f['hour'] = data_f['date'].dt.hour
    data_f['minute'] = data_f['date'].dt.minute
    data_f['month_num'] = data_f['date'].dt.month
    data_f['timeline_date'] = data_f['date'].dt.date
    data_f['day_name']=data_f['date'].dt.day_name()

    period = []
    for hour in data_f[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str(hour + 1))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    data_f['period'] = period

    return data_f
