from nltk.stem.porter import PorterStemmer
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
def topicizer(text):
    stopWords = set(stopwords.words("english"))
    all_words = word_tokenize(text)
    for i in range(len(all_words)):
        all_words[i] = all_words[i].lower()
    for word in all_words:
        if word in stopWords or word == '.' or word == ',':
            all_words.remove(word)
    all_words = [PorterStemmer().stem(word) for word in all_words]
    word_frequency = dict()
    for word in all_words:
        if word in word_frequency:
            word_frequency[word] += 1
        else:
            word_frequency[word] = 1
    max_num = 0
    topic = ''
    for word in word_frequency:
        if word_frequency[word] > max_num:
            topic = word
        if word_frequency[word] == max_num:
            topic += ' ' + word
    return(topic)
