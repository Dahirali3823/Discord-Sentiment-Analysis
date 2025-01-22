import json
import numpy as np
import matplotlib.pyplot as plt
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from wordcloud import WordCloud

analyzer = SentimentIntensityAnalyzer()
nltk.download('stopwords')
# Load the existing data from the JSON file
with open('/Users/dahirali/Desktop/Sentiment analysis/Samplemessages.json', 'r', encoding='utf-8') as f:
    existing_data = json.load(f)


def plot_piechart(sentiment_scores, ax):
    neg = 0
    pos = 0
    neu = 0
    # Get neg, pos, neutral, compound scores in arrays
    for score_dict in sentiment_scores:
        if score_dict['neg'] > score_dict['pos'] and score_dict['neg'] > score_dict['neu']:
            neg += 1
        elif score_dict['pos'] > score_dict['neg'] and score_dict['pos'] > score_dict['neu']:
            pos += 1
        else:
            neu += 1
    # Plot pie chart
    x = np.array([pos, neg, neu])
    label = ["Positive", "Negative", "Neutral"]
    ax.pie(x, labels=label, autopct='%1.1f%%')
    ax.set_title("Sentiment Distribution")


def plot_barchart(sentiment_scores, ax):
    neg = []
    pos = []
    neu = []
    # Get neg, pos, neutral, compound scores in arrays
    for score_dict in sentiment_scores:
        neg.append(score_dict['neg'])
        pos.append(score_dict['pos'])
        neu.append(score_dict['neu'])
   
    positive = sum(pos) / len(pos)
    negative = sum(neg) / len(neg)
    neutral = sum(neu) / len(neu)

    sentiment = [positive, negative, neutral]
    Tone = ["Positive", "Negative", "Neutral"]

    # Plot bar chart
    ax.bar(Tone, sentiment)
    ax.set_title("Average Sentiment")
    ax.set_xlabel("Sentiment")
    ax.set_ylabel("Score")


def topwords(existing_data, ax):
    dictionary = {}

    
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
    top_10 = list(sorted_dict.items())[:10]

    # Separate words and counts for the table
    words, counts = zip(*top_10)

    # Create a table on the given axis
    table_data = list(zip(words, counts))
    table = ax.table(cellText=table_data, colLabels=['Word', 'Count'], loc='center')
    ax.axis('tight')
    ax.axis('off')
    ax.set_title("Top 10 Words")



def plot_wordcloud():
    # Combine all words from the existing data
    text = ' '.join(existing_data)
    test = set(stopwords.words('english'))
    # Generate a word cloud
    wordcloud = WordCloud(stopwords=test, background_color="white").generate(text)
    
    # Plot the word cloud
    plt.figure(figsize=(8, 8))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.title("Word Cloud of Top Words")
    plt.show()

# Sentiment analysis
sentiment_scores = []
for text in existing_data:
    scores = analyzer.polarity_scores(text)
    sentiment_scores.append(scores)

# Create subplots (1 row, 3 columns)
fig, axs = plt.subplots(1, 3, figsize=(15, 6))  # Adjusted the figsize to make it smaller

# Plot the pie chart, bar chart, and word frequency table
plot_piechart(sentiment_scores, axs[0])
plot_barchart(sentiment_scores, axs[1])
topwords(existing_data, axs[2])
plot_wordcloud()

# Adjust layout and display the plots
plt.tight_layout()
plt.show()
