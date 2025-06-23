from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji

extract = URLExtract()

# function for specific user stats
def fetch_stats(selected_user, df):

    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    # fetch total number of messages
    num_messages = df.shape[0]

    # fetch total number of words
    words = []
    for message in df['message']:
        words.extend(message.split())

    # fetch total number of media
    num_media = df[df['message'] == '<Media omitted>\n'].shape[0]

    # fecth total number of links
    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))

    return num_messages, len(words), num_media, len(links)

# function for group analysis
def most_busy_users(df):
    mostBusyUsers = df['user'].value_counts().head()
    busyPercent = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(columns={'count':'percent'})
    return mostBusyUsers, busyPercent

# for Word Cloud Image
def createWordCloud(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    df = df[df['user'] != 'group_notification']
    df = df[df['message'] != "<Media omitted>\n"] # media messages removed

    wc = WordCloud(width=500, height=500, min_font_size=12, background_color='white')
    df_wc = wc.generate(df['message'].str.cat(sep= ' '))
    return df_wc

# Most Common Words
def mostCommonWords(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != "<Media omitted>\n"]

    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()
    f.close()

    words = []

    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    mostCommon = pd.DataFrame(Counter(words).most_common(20))
    return mostCommon

# Emoji function
def emojiHelper(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        for c in message:
            if c in emoji.EMOJI_DATA:
                emojis.extend(c)

    emoji_df = pd.DataFrame(Counter(emojis).most_common(), columns=['Emoji', 'Used Count'])

    return emoji_df

# Monthly Timeline
def monthlyTimeline(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]
    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + '-' + str(timeline['year'][i]))
    timeline['time'] = time

    return timeline

# activity map
def activityMap(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    weekly_df = df['day_name'].value_counts()
    monthly_df = df['month'].value_counts()
    return weekly_df, monthly_df

def activityHeatmap(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)

    return user_heatmap