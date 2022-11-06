import streamlit as st
import preprocess_chat, helper, chat_sentiment_analyze
import matplotlib.pyplot as plt
import seaborn as sns
import requests
import streamlit.components.v1 as components

from PIL import Image
logo = Image.open('ChatDat-logo.png')
#st.sidebar.title("ChatDat - Analyze Your Chats Data")
st.markdown("<h1 style='text-align: center; color: #4267B2;'>ChatDat</h1><h5 style='text-align: center; color: #898F9C;'>Analyze Your Chats Data</h5>", unsafe_allow_html=True)

st.sidebar.image(logo)

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocess_chat.preprocess(data)

    # we need users list to make a drop down for selection for analysis
    # fetch unique users
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,"Overall")

    selected_user = st.sidebar.selectbox("Show analysis wrt",user_list)

    if st.sidebar.button("Show Analysis"):
        with st.spinner('All are computing, kindly Wait for it...'):
            #Sentiment Analysis
            st.title("The Sentiment Analysis: ")
            if(selected_user == 'Overall'):
                df_sent = df
                st.subheader("Whole Chat")
            else:
                df_sent = df[df['user']== selected_user]
                st.subheader("Filtered based on user: " + selected_user)

            df_sent = chat_sentiment_analyze.sentiment_analysis(df_sent)

            st.text("To look the Sentiment Scores of each chat - Scroll horizontally and vertically ")
            df_sent = df_sent.drop(columns=['month', 'day', 'hour', 'minute','year','only_date','month_num','day_name', 'period'])
            lst = []
            for i in range(df_sent.shape[0]):
                lst.append("")
            
            df_sent["Result"] = lst

            for ind in df_sent.index:
                a=df_sent["Positive"][ind]
                b=df_sent["Negative"][ind]
                c=df_sent["Neutral"][ind]

                if (a>b) and (a>c):
                    df_sent["Result"][ind] = "Positive"
                if (b>a) and (b>c):
                    df_sent["Result"][ind] = "Negative"
                if (c>a) and (c>b):
                    df_sent["Result"][ind] = "Neutral"

            st.write(df_sent)   

            result = chat_sentiment_analyze.sentiment_overall(df_sent)
            st.header("The Overall Sentiment Analysis : "+result )
            st.write("This is based on the arithmetic calculation of sentiment analysis score of the overall filtered chats")
            
            st.markdown("<br><br><hr><br><br>", unsafe_allow_html=True)

            # Stats Area
            num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user,df)
            st.markdown("<h2>Top Statistics</h2>", unsafe_allow_html=True)
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.header("Total Messages")
                st.title(num_messages)
            with col2:
                st.header("Total Words")
                st.title(words)
            with col3:
                st.header("Media Shared")
                st.title(num_media_messages)
            with col4:
                st.header("Links Shared")
                st.title(num_links)
            
            st.markdown("<hr><br>", unsafe_allow_html=True)

            # monthly timeline
            st.title("Monthly Timeline")
            timeline = helper.monthly_timeline(selected_user,df)
            fig,ax = plt.subplots()
            ax.plot(timeline['time'], timeline['message'],color='green')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

            st.markdown("<hr><br>", unsafe_allow_html=True)

            # daily timeline
            st.title("Daily Timeline")
            daily_timeline = helper.daily_timeline(selected_user, df)
            fig, ax = plt.subplots()
            ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='black')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

            st.markdown("<hr><br>", unsafe_allow_html=True)

            # activity map
            st.title('Activity Map')
            col1,col2 = st.columns(2)

            with col1:
                st.header("Most busy day")
                busy_day = helper.week_activity_map(selected_user,df)
                fig,ax = plt.subplots()
                ax.bar(busy_day.index,busy_day.values,color='purple')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            with col2:
                st.header("Most busy month")
                busy_month = helper.month_activity_map(selected_user, df)
                fig, ax = plt.subplots()
                ax.bar(busy_month.index, busy_month.values,color='orange')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            
            st.markdown("<hr><br>", unsafe_allow_html=True)

            st.title("Weekly Activity Map")
            user_heatmap = helper.activity_heatmap(selected_user,df)
            fig,ax = plt.subplots()
            ax = sns.heatmap(user_heatmap)
            st.pyplot(fig)


            # finding the busiest users in the group(Group level)
            if selected_user == 'Overall':
                st.title('Most Busy Users')
                x,new_df = helper.most_busy_users(df)
                fig, ax = plt.subplots()

                col1, col2 = st.columns(2)

                with col1:
                    ax.bar(x.index, x.values,color='red')
                    plt.xticks(rotation='vertical')
                    st.pyplot(fig)
                with col2:
                    st.dataframe(new_df)

            st.markdown("<hr><br>", unsafe_allow_html=True)

            # WordCloud
            st.title("Wordcloud")
            df_wc = helper.create_wordcloud(selected_user,df)
            fig,ax = plt.subplots()
            ax.imshow(df_wc)
            st.pyplot(fig)
             
            # most common words
            most_common_df = helper.most_common_words(selected_user,df)

            fig,ax = plt.subplots()

            ax.barh(most_common_df[0],most_common_df[1])
            plt.xticks(rotation='vertical')

            st.markdown("<hr><br>", unsafe_allow_html=True)
            st.title('Most commmon words')
            st.pyplot(fig)

            st.markdown("<hr><br>", unsafe_allow_html=True)
            # emoji analysis
            emoji_df = helper.emoji_helper(selected_user,df)
            st.title("Emoji Analysis")

            col1,col2 = st.columns(2)

            with col1:
                st.dataframe(emoji_df)
            with col2:
                fig,ax = plt.subplots()
                st.write("Top 5 Emoji - Piechart")
                ax.pie(emoji_df['Count'].head(), labels = round(emoji_df['Count'].head(),2) ,autopct="%0.2f")
                st.pyplot(fig)

            st.markdown("<hr><br>", unsafe_allow_html=True)


#Removing the made by 
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

#Linkedin addition
embedcmp = { 'linkedin': """<script src="https://platform.linkedin.com/badges/js/profile.js" async defer type="text/javascript"></script> <div class="badge-base LI-profile-badge" data-locale="en_US" data-size="medium" data-theme="light" data-type="VERTICAL" data-vanity="balakrishnan-r-906404184" data-version="v1"><a class="badge-base__link LI-simple-link" href="https://in.linkedin.com/in/balakrishnan-r-906404184?trk=profile-badge">Balakrishnan R</a></div>"""
}

with st.sidebar:
    st.markdown("<br><hr><br><br>", unsafe_allow_html=True)
    st.subheader("Reach me out: ")
    st.write("The Developer: ")
    components.html(embedcmp['linkedin'],height=350)
