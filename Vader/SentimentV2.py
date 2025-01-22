#machine learning babyyyyy
#split data to 80/20 for trainig/testing random
#find model
#train it 
#test it 
#use it
import json
import numpy as np
import matplotlib.pyplot as plt
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
analyzer = SentimentIntensityAnalyzer()

with open('/Users/dahirali/Desktop/Sentiment analysis/Samplemessages.json', 'r', encoding='utf-8') as f:
    existing_data = json.load(f)


def plot_piechart(sentiment_scores):


    neg = 0
    pos = 0
    neu = 0
    # get neg, pos, neutral, compound scores in arrays
    for score_dict in sentiment_scores:

        if score_dict['neg'] > score_dict['pos'] and score_dict['neg'] > score_dict['neu']:
            neg += 1

        elif score_dict['pos'] > score_dict['neg'] and score_dict['pos'] > score_dict['neu']:
            pos += 1

        else:
            neu += 1
    # neg.append(score_dict['neg'])
    # pos.append(score_dict['pos'])
    # neu.append(score_dict['neu'])
    # comp.append(score_dict['compound'])


    x = np.array([pos, neg, neu])
    print("Pie chart pos",pos)
    print("Pie chart neg",neg)
    print("Pie chart neu",neu)
    plt.subplot(1,2,1)
    label = ["Positive", "Negative", "Neutral"]
    plt.pie(x, labels=label)
    plt.title("Sentiment Distribution")

def plot_barchart(sentiment_scores):
    neg = []
    pos = []
    neu = []
    # get neg, pos, neutral, compound scores in arrays
    for score_dict in sentiment_scores:
        neg.append(score_dict['neg'])
        pos.append(score_dict['pos'])
        neu.append(score_dict['neu'])
   
    positive = sum(pos)/len(pos)
    negative = sum(neg)/len(neg)
    neutral = sum(neu)/len(neu)

    sentiment = [positive, negative, neutral]
    Tone = ["Positive","Negative","Neutral"]

    print("Bar chart pos",positive)
    print("Bar chart neg",negative)
    print("Bar chart neu",neutral)
    
    plt.subplot(1,2,2)
    plt.bar(Tone, sentiment)
    plt.title("Average Sentiment")
    plt.xlabel("Sentiment")
    plt.ylabel("Score")
   

def topwords():
    dictionary = {}

    nltk.download('stopwords')
    test = set(stopwords.words('english'))

    # Loop through each sentence in the existing data
    for sentence in existing_data:
        words = word_tokenize(sentence)

        for word in words:
            word = word.lower()  # Convert to lowercase to handle case-insensitivity
            if word not in test and word.isalpha():  # Check if it's not a stopword and is alphabetic
                if word in dictionary:
                    dictionary[word] += 1
                else:
                    dictionary[word] = 1

    # Sort dictionary by count in descending order
    sorted_dict = dict(sorted(dictionary.items(), key=lambda item: item[1], reverse=True))

    # Get the top 10 words
    top_10 = list(sorted_dict.items())[:20]

    # Separate words and counts for the table
    words, counts = zip(*top_10)

    # Create a matplotlib table
    fig, ax = plt.subplots()
    ax.axis('tight')
    ax.axis('off')
    table_data = list(zip(words, counts))
    table = ax.table(cellText=table_data, colLabels=['Word', 'Count'], loc='center')

    # Display the table
    plt.show()

sentiment_scores = []
# Loop through the texts and get the sentiment scores for each one
for text in existing_data:
    scores = analyzer.polarity_scores(text)
    sentiment_scores.append(scores)


plt.figure(figsize=(12, 6)) 
plot_piechart(sentiment_scores)
plot_barchart(sentiment_scores)
topwords()

plt.tight_layout()  
plt.show()


#top 10 said words

#top 10 negative and postive words

#another cool graph