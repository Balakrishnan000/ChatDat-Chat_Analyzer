# ChatDat-Chat_Analyzer
A Data Analytics and Sentiment Analysis project with Dynamic Dataset that has been created by user on uploading the whatsapp chat data.

## ChatDat Architecture
![image](https://github.com/Balakrishnan000/ChatDat-Chat_Analyzer/assets/70379877/1fd943b2-7419-456d-ae9b-e2496e3c6ff2)

## A Live Demo and Quick Project Explanation
#### [Youtube Link - Click Here ](https://youtu.be/RvanjLbdb6Y)

## How to Host the Web Application?
1. Clone the repository into your local environment using command git clone https://github.com/Balakrishnan000/ChatDat-Chat_Analyzer.git <br>
2. Go to the Directory and on the terminal, run pip install -r requirements.txt All the required packages will now be installed.<br>
3. On the terminal, run py -m streamlit run app.py <br>

The web app will now be hosted on your localhost.
<br>
(OR)<br>
Hosted Version on Herouku:<br>
#### Live Link:[https://chatdat-bala000.streamlit.app/](https://chatdat-bala000.streamlit.app/)

## How to generate dataset?
![image](https://github.com/Balakrishnan000/ChatDat-Chat_Analyzer/assets/70379877/fe26dd21-ba63-4418-9817-7f767043a71f)

## Modules Built:
- Sentiment Analysis of individual filtered chats
- Sentiment Analysis overall
- Top Statistics
- Monthly timeline
- Daily timeline
- Activity map - Day wise, Month wise
- Weekly activity map
- Most Busy Users List generation
- WordCloud of the filtered chat
- Most Common words of filtered chat
- Emoji Analysis and Visualization
- File Uploader widget
- Contact us widget

## Performance Metrics:
The Sentiment Analysis is done on:
- Nltk library of python.
- Specifically we are using nltk.sentiment.vader
- VADER (F1 = 0.96)
- F1 score is a  mixture of recall and precision.
- Recall - tells How well the Positive samples are detected wrt ground truth.
- Precision - tells out of all predictions how many are correct Positive predictions.

## Requirements: (Python Libraries)
* streamlit
* matplotlib
* seaborn
* URLExtract
* WordCloud
* pandas
* emoji
* nltk
