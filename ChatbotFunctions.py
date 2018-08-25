import os
from NLP import *
from betterTopic import *
from time import *
from googlesearch import search
from nltk import sent_tokenize, tokenize, word_tokenize
from win10toast import ToastNotifier
import bs4
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
from weather import Weather, Unit
import re
from PyDictionary import PyDictionary
import winsound
import matplotlib
import matplotlib.pyplot
from tkinter import filedialog, Tk
import pandas as pd
import winsound
from autocorrect import spell
from sympy import *
dictionary=PyDictionary()
numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '(', ')', '*', '+', '-', '/']
def autocrct(prompt, join):
    prompt = prompt.split(' ')
    for i in range(len(prompt)):
        if (not isInt(prompt[i])) and (not isFormula(prompt[i])) and (not isUrl(prompt[i])) and (not isEqua(prompt[i])):
            prompt[i] = spell(prompt[i])
    if join:
        space = ' '
        joint = space.join(prompt)
        return(joint)
    return(prompt)
def isInt(string):
    try:
        int(string)
        return True
    except Exception:
        return False
def isFormula(str):
    try:
        sympify(str.split('=')[0])
        sympify(str.split('=')[1])
        return True
    except Exception:
        return False
def isUrl(str):
    if "www." in str or "https://" in str:
        return True
    else:
        return False
def isEqua(str):
    try:
        sympify(str)
        for i in numbers:
            if i in str:
                return True
        return False
    except Exception:
        return False
def gridX(n, t):
    t.color("silver")
    t.speed(0)
    t.penup()
    t.goto(n*25, -n*25)
    t.pendown()
    for i in range(-n*25, n*25, 25):
        if i == 0:
            t.color("black")
        else:
            t.color("silver")
        t.goto(n*25, i)
        t.pendown()
        t.goto(-n*25, i)
        t.penup()
        
def gridY(n, t):
    t.color("silver")
    t.speed(0)
    t.penup()
    t.goto(-n*25, n*25)
    t.pendown()
    for i in range(-n*25, n*25, 25):
        if i == 0:
            t.color("black")
        else:
            t.color("silver")
        t.goto(i, n*25)
        t.pendown()
        t.goto(i, -n*25)
        t.penup()

def Music(name):
    winsound.PlaySound(name, winsound.SND_ASYNC)
    return "Playing " + name

def StopMusic():
    winsound.PlaySound(None, winsound.SND_PURGE)
    return "Stopped All Music"
        
def definition(word):
    return(dictionary.meaning(word))

def remove_duplicates(values):
    output = []
    seen = set()
    for value in values:
        # If value has not been encountered yet,
        # ... add it to both list and set.
        if value not in seen:
            output.append(value)
            seen.add(value)
    return output
import nltk
from nltk.corpus import wordnet
def synonym(word):
    synonyms = []
    for syn in wordnet.synsets(word):
        for l in syn.lemmas():
            synonyms.append(l.name())
    return remove_duplicates(synonyms)
def antonym(word):
    antonyms = []
    for syn in wordnet.synsets(word):
        for l in syn.lemmas():
            if l.antonyms():
                antonyms.append(l.antonyms()[0].name())
    return remove_duplicates(antonyms)
def TopNews():
    news_url="https://news.google.com/news/rss"
    Client=urlopen(news_url)
    xml_page=Client.read()
    Client.close()
    soup_page=soup(xml_page,"xml")
    news_list=soup_page.findAll("item")
    # Print news title, url and publish date
    res = ''
    for news in news_list:
        res = res + news.title.text + "\n"
        res = res + news.link.text + "\n"
        res = res + news.pubDate.text + "\n"
        res = res + "-"*60 + "\n"
    return res
def ShutDown(sec):
    os.system("shutdown /s /t " + str(sec))
def Restart(sec):
    os.system("shutdown /r /t " + str(sec))
def OpenApp(app):
    os.system("start " + app)
def Timer(sec, action, root):
    toaster = ToastNotifier()
    def callback():
        toaster.show_toast("Alert","Ringgg... Time to " + action + "!!!")
    root.after(sec*1000, callback)
def CurrentWeather(WOEID):
    weather = Weather(unit=Unit.CELSIUS)
    lookup = weather.lookup(WOEID)
    condition = lookup.condition
    return condition
def Forecast(WOEID):
    weather = Weather(unit=Unit.CELSIUS)
    location = weather.lookup(WOEID)
    forecasts = location.forecast
    string = ''
    for forecast in forecasts:
        string = string + ("Weather: " + forecast.text) + "\n"
        string = string + ("Date: "+ forecast.date) + "\n"
        string = string + ("Highest Temperature: " + forecast.high) + "\n"
        string = string + ("Lowest Temperature: " + forecast.low) + "\n"
        string = string + ("-"*60) + "\n"
    return string
def Google(query, num):
    Result = []
    for url in search(query, tld="com", stop=num, pause=2.5):
        Result.append(url)
    return Result    
def Sentiment(file):
    f = open(file, "r")
    message = f.read()
    f.close()
    tokens = sent_tokenize(message)
    pos = SentimentAnalysis(tokens)
    res = []
    if(pos < -0.55):
        res.append("Very Negative")
    elif(-0.65 <= pos < -0.1):
        res.append("Moderately Negative")
    elif(-0.1 <= pos < 0.1):
        res.append("Neutral")
    elif(0.1 <= pos < 0.55):
        res.append("Moderately Positive")
    else:
        res.append("Very Positive")
    res.append(round(pos*100, 2))
def WebSentiment(url):
    pos = WebSentimentAnalysis([url])
    if(pos < -0.55):
        res.append("Very Negative")
    elif(-0.65 <= pos < -0.1):
        res.append("Moderately Negative")
    elif(-0.1 <= pos < 0.1):
        res.append("Neutral")
    elif(0.1 <= pos < 0.55):
        res.append("Moderately Positive")
    else:
        res.append("Very Positive")
    res.append(round(pos*100, 2))
    
def WebTopic(url):   
    return str(str(ObtainTopics(url)[0][1][0][0]))

def TextTopic(file):
    f = open(file, "r")
    message = f.read()
    f.close()
    return str(topicizer(message))
def TextSummary(file):
    with open(file, 'r') as myfile:
        text = myfile.read().replace('\n', ' ')
    return(summarizer(text))
def WebSummary(url):
    text = parasParser(url, False)
    text = text.replace('\n', ' ')
    text = text.replace('\t', ' ')
    return(summarizer(text))
from nltk.corpus import stopwords
def textFix(text):
    result = text.replace("?", "? ")
    return result
def Fact(prom):
    stopWords = set(stopwords.words("english"))
    stopWords.add('is')
    try:
        text = parasParser(Google(prom, 1)[0], True)
        words = word_tokenize(prom)
        for word in words:
            word.lower()
            if word in stopWords:
                words.remove(word)
                continue
            try:
                for i in synonym(word):
                    word.append(i)
            except Exception:
                pass
        wordfound = 0
        large = 0
        largein = 0
        for i in range(len(text)):
            wordsfound = 0
            text[i].lower()
            if len(text[i]) > 500 or text[i].find('.') == -1 or i == 0 or i > len(text)-3:
                print(i)
                continue
            for j in range(len(words)):
                if words[j] in text[i]:
                    wordsfound += 1
                if wordsfound > large:
                    largein = i
                    large = wordsfound
        try:
            return textFix(text[largein])
        except Exception:
            return "Umm... IDK"
    except Exception:
        return "Umm... IDK"
import numpy
import math
def cal(expr):
    expr = expr.replace("^", "**")
    expr = sympify(expr)
    return expr.evalf()
def graph(formula, start, stop, t):
    formula = formula.replace("^", "**")
    t.color("black")
    XCors = list(range(start, stop+1))
    YCors = []
    x, y = symbols("x y")
    formula = Eq(sympify(formula.split('=')[0]), sympify(formula.split('=')[1]))
    formula = solve(formula, y)
    formula = formula[0]
    expr = formula
    for i in range(len(XCors)):
        expr = str(formula).replace("x", str(XCors[i]))
        expr2 = sympify(expr)
        YCors.append(expr2.evalf())
    t.penup()
    t.goto(int(XCors[0]), int(YCors[0]))
    t.pendown()
    for i in range(len(XCors)):
        try:
            t.goto(int(XCors[i]), int(YCors[i]))
        except Exception:
            return "The graph has generated complex numbers"
    return "Graphing Equation Now"
def CreateList(name):
    zero = [0]
    Data = pd.DataFrame(data={name : zero})
    Data.to_csv(name + ".csv")
def AddList(name, obj):
    try:
        Data = pd.read_csv(name + ".csv")
    except Exception:
        return "This file does not exist"
    dataList = Data[name].tolist()
    dataList.append(obj)
    Data = pd.DataFrame(data = {name : dataList})
    Data.to_csv(name + ".csv")
    return "Added successfully"
def RemoveList(name, obj):
    try:
        Data = pd.read_csv(name + ".csv")
    except Exception:
        return "This file does not exist"
    dataList = Data[name].tolist()
    try:
        ind = dataList.index(obj)
        del dataList[ind]
    except Exception:
        return "There is no such thing in that list :("
    Data = pd.DataFrame(data = {name : dataList})
    Data.to_csv(name + ".csv")
    return "Successfully removed"
def GetList(name):
    try:
        Data = pd.read_csv(name + ".csv")
    except Exception:
        return "This file does not exist"
    dataList = Data[name].tolist()
    return dataList
    return ""
def ExtractRubbish(file, newfile, column): #filter swear words
    arrBad = pd.read_csv(SwearLib)
    Data = pd.read_csv(file)
    
    try:
        List = Data[column].tolist()
    except Exception:
        return "The column is not found"
    
    RemoveCount = 0
    for i in range(len(List)):
        for bad in arrBad:
            if (" " + bad + " ") in List[i - RemoveCount].lower():
                Data.drop(Data.index[i - RemoveCount], inplace = True)
                print(List[i - RemoveCount])
                del List[i - RemoveCount]
                RemoveCount += 1
                break
    Data.to_csv(newfile)
    return "The file has been cleaned"
def ExtractInts(file, column, newcolumn):
    Append = True
    One = ['one', 'once']
    Two = ['two', 'twice', 'double']
    Three = ['three', 'thrice']
    Four = ['four']
    Five = ['five']
    Six = ['six']
    Seven = ['seven', 'daily', 'everyday', 'every']
    Eight = ['eight']
    Nine = ['nine']
    Zero = ['never', 'rarely', 'zero', 'uncommon']
    Nums = [Zero, One, Two, Three, Four, Five, Six, Seven, Eight, Nine]
    Data = pd.read_csv(file)
    try:
        List = Data[column].tolist()
    except Exception:
        return "The column is not found"
    tokens = []
    ListNum = []
    print(List)
    for i in List:
        tokens = word_tokenize(autocrct(i, True))
        Append = True
        for word in tokens:
            for num in range(len(Nums)):
                for n in Nums[num]:
                    if n == word.lower():
                        print(word.lower())
                        ListNum.append(num)
                        Append = False
                        break
                    elif isInt(word.lower()):
                        ListNum.append(int(word.lower()))
                        Append = False
                        break
                else:
                    continue
                break
            else:
                continue
            break
        if Append:
            ListNum.append(0)
    Data[newcolumn] = ListNum
    Data.to_csv(file)
    return "The integers have been extracted"
def ExtractSentiment(file, column, newcolumn):
    Data = pd.read_csv(file)
    try:
        List = Data[column].tolist()
    except Exception:
        return "The column is not found"
    res=[]
    for i in List:
        tokens = sent_tokenize(autocrct(i, True))
        pos = SentimentAnalysis(tokens)
        res.append(round(pos*100, 2))
    Data[newcolumn] = res
    Data.to_csv(file)
    return "The sentiment has been successfully"
def ExtractTopic(file, column, newcolumn):
    Data = pd.read_csv(file)
    try:
        List = Data[column].tolist()
    except Exception:
        return "The column is not found"
    res=[]
    for i in List:
        res.append(topicizer(autocrct(i, True)))
    Data[newcolumn] = res
    Data.to_csv(file)
    return "The topics have been successfully extracted"
def PlotScatterData(file, column, column2):
    Data = pd.read_csv(file)
    try:
        x = Data[column].tolist()
        y = Data[column2].tolist()
    except Exception:
        return "The column is not found"
    plt = matplotlib.pyplot.scatter(x, y, c='b')
    z = numpy.polyfit(x, y, 2)
    matplotlib.pyplot.plot(x,numpy.polyval(z,x))
    matplotlib.pyplot.show()
    return "The scatter plot has been plotted"
def PlotGraphData(file, column, column2):
    Data = pd.read_csv(file)
    try:
        x = Data[column].tolist()
        y = Data[column2].tolist()
    except Exception:
        return "The column is not found"
    plt = matplotlib.pyplot.plot(x, y, c='b')
    z = numpy.polyfit(x, y, 2)
    matplotlib.pyplot.plot(x,numpy.polyval(z,x))
    matplotlib.pyplot.show()
    return "The graph has been plotted"
def PlotPieData(file, column, labels):
    Data = pd.read_csv(file)
    try:
        Pie = Data[column].tolist()
    except ZeroDivisionError:
        return "The column is not found"
    matplotlib.pyplot.pie(Pie, labels=labels)
    matplotlib.pyplot.axis("equal")
    matplotlib.pyplot.show()
    return "The Pie Chart has been drawn"
#Algebra
def simplifyEqu(equation):
    equation = equation.replace("^", "**")
    a, b, c, d, e, m, n, o, p, u, x, y, z = symbols('a b c d e m n o p u x y z')
    expr = sympify(equation)
    return simplify(expr)
def solveEqu(equation, equation2, var, evalu):
    equation = equation.replace("^", "**")
    equation2 = equation2.replace("^", "**")
    a, b, c, d, e, m, n, o, p, u, x, y, z = symbols('a b c d e m n o p u x y z')
    expr = sympify(equation)
    expr2 = sympify(equation2)
    var = sympify(var)
    if evalu == True:
        solution = solve(Eq(expr, expr2), var)
        result = []
        for i in solution:
            result.append(i.evalf())
        return result
    else:
        return solve(Eq(expr, expr2), var)
def expandEqu(equation):
    equation = equation.replace("^", "**")
    a, b, c, d, e, m, n, o, p, u, x, y, z = symbols('a b c d e m n o p u x y z')
    expr = sympify(equation)
    return expand(expr)
def factoriseEqu(equation):
    equation = equation.replace("^", "**")
    a, b, c, d, e, m, n, o, p, u, x, y, z = symbols('a b c d e m n o p u x y z')
    expr = sympify(equation)
    return factor(expr)
#Calculus
def limitCal(equation, var):
    equation = equation.replace("^", "**")
    a, b, c, d, e, m, n, o, p, u, x, y, z = symbols('a b c d e m n o p u x y z')
    expr = sympify(equation)
    varia = sympify(var)
    return limit(expr, varia, oo)
def diffCal(equation, var):
    equation = equation.replace("^", "**")
    a, b, c, d, e, m, n, o, p, u, x, y, z = symbols('a b c d e m n o p u x y z')
    expr = sympify(equation)
    varia = sympify(var)
    return diff(expr, varia)
def integrateCal(equation, var):
    equation = equation.replace("^", "**")
    a, b, c, d, e, m, n, o, p, u, x, y, z = symbols('a b c d e m n o p u x y z')
    expr = sympify(equation)
    varia = sympify(var)
    return integrate(expr, varia) 
#Geometry
import turtle as t1
def TriangleArea(x, y, x2, y2, x3, y3, evalu, can):
    t = t1.RawTurtle(can)
    t.color('black')
    t.penup()
    t.goto(x, y)
    t.pendown()
    t.goto(x2, y2)
    t.goto(x3, y3)
    t.goto(x, y)
    a = Point(x, y)
    b = Point(x2, y2)
    c = Point(x3, y3)
    t = Triangle(a, b, c)
    if(evalu == True):
        try:
            return abs((t.area).evalf())
        except Exception:
            return "This is Not A Valid Triangle"
    else:
        try:
            return abs(t.area)
        except Exception:
            return "This is Not A Valid Triangle"
        
def TrianglePerimeter(x, y, x2, y2, x3, y3, evalu, can):
    t = t1.RawTurtle(can)
    t.color('black')
    t.penup()
    t.goto(x, y)
    t.pendown()
    t.goto(x2, y2)
    t.goto(x3, y3)
    t.goto(x, y)
    a = Point(x, y)
    b = Point(x2, y2)
    c = Point(x3, y3)
    t = Triangle(a, b, c)
    if(evalu == True):
        try:
            return abs((t.perimeter).evalf())
        except Exception:
            return "This is Not A Valid Triangle"
    else:
        try:
            return abs(t.perimeter)
        except Exception:
            return "This is Not A Valid Triangle"

def TriangleEqul(x, y, x2, y2, x3, y3, can):
    t = t1.RawTurtle(can)
    t.color('black')
    t.penup()
    t.goto(x, y)
    t.pendown()
    t.goto(x2, y2)
    t.goto(x3, y3)
    t.goto(x, y)
    a = Point(x, y)
    b = Point(x2, y2)
    c = Point(x3, y3)
    t = Triangle(a, b, c)
    try:
        return t.is_equilateral()
    except Exception:
        return False

def TriangleIsos(x, y, x2, y2, x3, y3, can):
    t = t1.RawTurtle(can)
    t.color('black')
    t.penup()
    t.goto(x, y)
    t.pendown()
    t.goto(x2, y2)
    t.goto(x3, y3)
    t.goto(x, y)
    a = Point(x, y)
    b = Point(x2, y2)
    c = Point(x3, y3)
    t = Triangle(a, b, c)
    try:
        return t.is_isoceles()
    except Exception:
        return False

def TriangleRight(x, y, x2, y2, x3, y3, can):
    t = t1.RawTurtle(can)
    t.color('black')
    t.penup()
    t.goto(x, y)
    t.pendown()
    t.goto(x2, y2)
    t.goto(x3, y3)
    t.goto(x, y)
    a = Point(x, y)
    b = Point(x2, y2)
    c = Point(x3, y3)
    t = Triangle(a, b, c)
    try:
        return t.is_right()
    except Exception:
        return False
        
def Colinear(x, y, x2, y2, x3, y3):
    a = Point(x, y)
    b = Point(x2, y2)
    c = Point(x3, y3)
    return Point.is_colinear(a, b, c)

from sympy.physics.units import *
import sys

def UnitConvert(val, unit, unit2):
    return convert_to(sympify(val)*sympify(str_to_class(unit)), sympify(str_to_class(unit2))).n()

def str_to_class(str):
    return getattr(sys.modules[__name__], str)
'''
#Chem
from chempy import *
def SubMass(formula):
    return Subtance.from_formula(formula).mass

def SubCharge(formula):
    return Subtance.from_formula(formula).charge

def IonicStrength(sub, sub2, num, num2):
    return ionic_strength({sub: num, sub2: num})
'''
