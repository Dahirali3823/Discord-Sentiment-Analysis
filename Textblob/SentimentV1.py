from textblob import TextBlob
import json
with open('/Users/dahirali/Desktop/Sentiment analysis/Samplemessages.json', 'r', encoding='utf-8') as f:
         existing_data = json.load(f)

def sentiment(message):
    m = TextBlob(message)
    value = m.sentiment.polarity
    return value

total = 0
count  = 0
for i in existing_data:
    polarity = sentiment(i)
    if polarity != 0.0:
        total += polarity
        count+=1
    #testing random polarities
    if polarity == -0.7:
        print(i)
average = total/count
print("The average polarity is",average)


