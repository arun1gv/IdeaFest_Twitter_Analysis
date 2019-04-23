from flask import Flask, render_template, request
import sys, tweepy, csv, re
from textblob import TextBlob
import matplotlib.pyplot as plt
import mpld3
from twitter_analysis import SentimentAnalysis

app = Flask(__name__)


def plotPieChart(positive, wpositive, spositive, negative, wnegative, snegative, neutral, searchTerm,
                 noOfSearchTerms):
    labels = ['Positive [' + str(positive) + '%]', 'Weakly Positive [' + str(wpositive) + '%]',
              'Strongly Positive [' + str(spositive) + '%]', 'Neutral [' + str(neutral) + '%]',
              'Negative [' + str(negative) + '%]', 'Weakly Negative [' + str(wnegative) + '%]',
              'Strongly Negative [' + str(snegative) + '%]']
    sizes = [positive, wpositive, spositive, neutral, negative, wnegative, snegative]
    colors = ['yellowgreen', 'lightgreen', 'darkgreen', 'gold', 'red', 'lightsalmon', 'darkred']
    patches, texts = plt.pie(sizes, colors=colors, startangle=90)
    plt.legend(patches, labels, loc="best")
    plt.title('How people are reacting on ' + searchTerm + ' by analyzing ' + str(noOfSearchTerms) + ' Tweets.')
    plt.axis('equal')
    plt.tight_layout()
    mpld3.show()
    #mpld3.fig_to_html(plt, d3_url = "http://127.0.0.1:8888/", mpld3_url= "http://127.0.0.1:8888/")


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/getSentiment', methods=['POST'])
def getSentiment():
    tweet = request.form['tweet']
    count = int(request.form['count'])
    sa = SentimentAnalysis()
    sentiment = sa.doSentimetAnalysis(tweet, count)
    # return render_template('success.html', tweet=tweet, count=count, negative=sentiment[3])
    return plotPieChart(sentiment[0], sentiment[1], sentiment[2], sentiment[3], sentiment[4], sentiment[5],
                        sentiment[6], tweet, count)


if __name__ == '__main__':
    app.run(port=8888)
