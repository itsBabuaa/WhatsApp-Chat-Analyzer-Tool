import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt
import seaborn as sns


#st.title('WhatsApp Chat Analyzer')
st.markdown(
        "<h1 style='color: green;'>WhatsApp Chat Analyzer!!</h1>",
        unsafe_allow_html=True
    )

st.sidebar.title("WhatsApp Chat Analyzer🔰")
upload_file = st.sidebar.file_uploader('Choose a file')

if upload_file is not None:
    bytes_data = upload_file.getvalue()
    data = bytes_data.decode("utf-8")
    #st.text(data)
    df = preprocessor.preprocess(data)

    #st.text('Uploaded Chat Data')
    st.dataframe(df)

    # fetch unique users
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("Show Analysis Of User", user_list)

    if st.sidebar.button("Show Analysis"):

        st.title("Analysis Report For " + selected_user)
        num_messages, words, num_media, num_links = helper.fetch_stats(selected_user, df)

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)

        with col2:
            st.header("Total Words")
            st.title(words)

        with col3:
            st.header("Media Shared")
            st.title(num_media)

        with col4:
            st.header("Links Shared")
            st.title(num_links)

        # Monthly Timeline
        st.title("Monthly Msg Timeline")
        timeline= helper.monthlyTimeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'], color='orange')
        plt.xlabel('Time')
        plt.ylabel('No. of Msg')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # Activity Map
        st.title('Activity Map')
        busyDay, busyMonth = helper.activityMap(selected_user, df)
        col1, col2 = st.columns(2)

        with col1:
            st.header("Most Busy Day")

            fig, ax = plt.subplots()
            ax.bar(busyDay.index, busyDay.values, color= 'teal')
            plt.xlabel('Day')
            plt.ylabel('No. of Msg')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header("Most Busy Month")

            fig, ax = plt.subplots()
            ax.bar(busyMonth.index, busyMonth.values, color='teal')
            plt.xlabel('Month')
            plt.ylabel('No. of Msg')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        st.title("Weekly Activity Map")
        user_heatmap = helper.activityHeatmap(selected_user, df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)

        # group level analysis
        if selected_user == 'Overall':
            st.title("Most Busy Users")
            mostBusyUsers, busyPercent = helper.most_busy_users(df)

            st.text('Top 5 Active Users')
            col1, col2 = st.columns(2)

            with col1:
                st.dataframe(mostBusyUsers)

            with col2:
                fig1, ax1 = plt.subplots()
                ax1.bar(mostBusyUsers.index, mostBusyUsers.values)
                plt.xticks(rotation='vertical')
                ax1.set_ylabel("No. of Msg")
                ax1.set_xlabel("Top 5 User")
                st.pyplot(fig1)

            st.text('Users And Activity Share')
            col1, col2 = st.columns(2)

            with col1:
                st.dataframe(busyPercent)

            with col2:
                # Pie Chart Plot
                fig2, ax2 = plt.subplots()
                ax2.pie(
                    busyPercent['percent'],
                    labels=busyPercent['user'],
                    autopct='%1.2f%%',
                    startangle= 90,
                )
                ax2.axis('equal')
                st.pyplot(fig2)


        # Word Cloud Analysis
        st.title("Word Cloud")
        df_wc = helper.createWordCloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        #Most Common Words
        st.title("Most Common Words")
        mostCommonWords = helper.mostCommonWords(selected_user, df)

        fig, ax = plt.subplots()

        ax.barh(mostCommonWords[0], mostCommonWords[1])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # Emoji Analysis
        st.title('Emoji Stats')
        emoji_df = helper.emojiHelper(selected_user, df)

        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig, ax = plt.subplots()
            ax.pie(emoji_df['Used Count'].head(), labels=emoji_df['Emoji'].head(), autopct="%0.2f")
            st.pyplot(fig)