import requests
from bs4 import BeautifulSoup
from selectolax.parser import HTMLParser
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
import string
import gensim
from gensim import corpora
import re

html = ""
tree = ""
Url = ""
parsed = False
def Text2(url, tokenize):
    global tree
    global html
    global parsed
    if (Url != url):
        parsed = False
    if parsed == False:
        html = requests.get(url).content
        tree = HTMLParser(html)
        parsed = True
    """
    soup = BeautifulSoup(html, 'html.parser')
    #soup = soup.find_all(string=lambda text:isinstance(text,Comment))

    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()    # rip it out

    # get text
    text = soup.get_text()

    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)
    text = soup.
    """

    if tree.body is None:
        return None

    for tag in tree.css('script'):
        tag.decompose()
    for tag in tree.css('style'):
        tag.decompose()

    text = tree.body.text(separator='\n')
    text = text.replace("\n", "")
    text = re.sub("[\(\[].*?[\)\]]", "", text)
    text = re.sub(r"\s+", " ", text)
    if tokenize==True:
        tokens = nltk.sent_tokenize(text)
        return tokens
    else:
        return text

def parasParser(url, tokenize):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    paras = soup.find_all('p')
    text = ''
    for para in paras:
        text += ' ' + str(para.getText())
    text = re.sub("[\(\[].*?[\)\]]", "", text)
    text = re.sub(r"\s+", " ", text)
    if tokenize:
        return(nltk.sent_tokenize(text))
    return(text)
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

def WebSentimentAnalysis(inputvar):
    for webpage in inputvar:
        totalSentences, TotalSentiment = 0, 0
        sid = SentimentIntensityAnalyzer()

        try:
            parsedWebpage = Text(webpage, True)
        except Exception:
            return None
        for sentence in parsedWebpage:
             ss = sid.polarity_scores(sentence)
             totalSentences += 1
             TotalSentiment += ss['compound']
    if totalSentences != 0:
        return (TotalSentiment / totalSentences)
    else:
        return "Error 404 - Not Found"
    
def SentimentAnalysis(inputvar):
    totalSentences, TotalSentiment = 0, 0
    sid = SentimentIntensityAnalyzer()
    for sentence in inputvar:
         ss = sid.polarity_scores(sentence)
         totalSentences += 1
         TotalSentiment += ss['compound']
    if totalSentences != 0:
        return (TotalSentiment / totalSentences)
    else:
        return "Error 404 - Not Found"


def clean(doc, stop, exclude, lemma):
    stop_free = " ".join([i for i in doc.lower().split() if i not in stop])
    punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
    normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
    return normalized

def get_list_of_lists(list_of_tuples):
    list_of_lists = []                                                          
    for tuple in list_of_tuples:
        list_of_lists.append(list(tuple))

    return list_of_lists

def ObtainTopics(url):
    doc_complete = [Text2(url, False)]
    
    stop = set(stopwords.words('english'))
    exclude = set(string.punctuation) 
    lemma = WordNetLemmatizer()

    doc_clean = [clean(doc, stop, exclude, lemma).split() for doc in doc_complete]

    # Creating the term dictionary of our courpus, where every unique term is assigned an index.
    dictionary = corpora.Dictionary(doc_clean)
    
    # Converting list of documents (corpus) into Document Term Matrix using dictionary prepared above.
    doc_term_matrix = [dictionary.doc2bow(doc) for doc in doc_clean]
    
    # Creating the object for LDA model using gensim library
    Lda = gensim.models.ldamodel.LdaModel

    try:
        doc_complete1 = ' '
        for i in range(len(doc_complete)):
            doc_complete1 = doc_complete1 + doc_complete[i]
        doc_complete1 = doc_complete1.replace(" ", "")
        # Running and Trainign LDA model on the document term matrix.
        if doc_complete1 != "":
            ldamodel = Lda(doc_term_matrix, num_topics=1, id2word = dictionary, passes=50)
            ldaTopic = ldamodel.show_topics(num_topics=1, num_words=1, log=False, formatted=False)
    
            return ldaTopic
        else:
            return [[0, [["Error 404 - Not Found"]]]]
        
    except Exception:
        return [[0, [["Error 404 - Not Found"]]]]

def ObtainTopics2(doc_complete):
    
    stop = set(stopwords.words('english'))
    exclude = set(string.punctuation) 
    lemma = WordNetLemmatizer()

    doc_clean = [clean(doc, stop, exclude, lemma).split() for doc in doc_complete]

    # Creating the term dictionary of our courpus, where every unique term is assigned an index.
    dictionary = corpora.Dictionary(doc_clean)
    
    # Converting list of documents (corpus) into Document Term Matrix using dictionary prepared above.
    doc_term_matrix = [dictionary.doc2bow(doc) for doc in doc_clean]
    
    # Creating the object for LDA model using gensim library
    Lda = gensim.models.ldamodel.LdaModel

    try:
        doc_complete1 = ' '
        for i in range(len(doc_complete)):
            doc_complete1 = doc_complete1 + doc_complete[i]
        doc_complete1 = doc_complete1.replace(" ", "")
        # Running and Trainign LDA model on the document term matrix.
        if doc_complete1 != "":
            ldamodel = Lda(doc_term_matrix, num_topics=1, id2word = dictionary, passes=50)
            ldaTopic = ldamodel.show_topics(num_topics=1, num_words=1, log=False, formatted=False)
    
            return ldaTopic
        else:
            return [[0, [["Error 404 - Not Found"]]]]
        
    except Exception:
        return [[0, [["Error 404 - Not Found"]]]]

from nltk.stem.porter import PorterStemmer
from nltk.tokenize import word_tokenize, sent_tokenize
def summarizer(text):
    stopWords = set(stopwords.words("english"))
    all_words = word_tokenize(text)
    all_words = [PorterStemmer().stem(word) for word in all_words]
    word_frequency = dict()
    sentences = sent_tokenize(text)
    sentenceValue = dict()
    for word in all_words:
        word = word.lower()
        if word in stopWords:
            continue
        if word in word_frequency:
            word_frequency[word] += 1
        else:
            word_frequency[word] = 1
    for sentence in sentences:
        for index, wordValue in enumerate(word_frequency, start=1):
            if wordValue in sentence.lower():
                if sentence in sentenceValue:  
                        sentenceValue[sentence] += index
                else:
                        sentenceValue[sentence] = index
    for sentence in sentenceValue:
        sentenceValue[sentence] = int(sentenceValue[sentence]/len(sentence))
    sumValues = 0
    for sentence in sentenceValue:
        sumValues += sentenceValue[sentence]

    average = int(sumValues/ len(sentenceValue))
    summary = ''
    for sentence in sentences:
            if sentence in sentenceValue and sentenceValue[sentence] > (1.2*average):
                summary += " " + sentence
    return(summary)
