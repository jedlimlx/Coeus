from autocorrect import spell
from nltk.tokenize import word_tokenize
from ChatbotFunctions import *
import os.path
from tkinter import *
from tkinter import filedialog
from turtle import *
import threading
import speech_recognition as sr
import time
from sympy import *
import yweather
from tkinter import ttk

Input = False
Start = True
InputResult = ''

r = sr.Recognizer()
mic = sr.Microphone()
def SpeechReg():
    while True:
        try:
            with mic as source:
                r.adjust_for_ambient_noise(source)
                audio = r.listen(source)
            Text = r.recognize_google(audio)
            break
        except Exception:
            Print("I do not understand you.")
    BoxText.set(Text)
    ButtonSend.invoke()

def FileGet():
    root2 = Tk()
    root2.filename =  filedialog.askopenfilename(initialdir = "/",title = "Select file", filetypes = (("wav Files", "*.wav"),("csv Files", "*.csv"),("text Files", "*.txt"),("All Files", "*.*")))
    text = root2.filename
    root2.destroy()
    return text

def GetInput(Question):
    global Input
    Output = ""
    Input = False
    var.set(0)
    Conversation.config(state=NORMAL)
    Conversation.insert(END, Question, 'tag-left')
    Conversation.insert(END, "\n\n")
    ButtonSend.wait_variable(var)
    Conversation.insert(END, TextBox.get(), 'tag-right')
    Conversation.insert(END, "\n\n")
    return TextBox.get()

def solve(prompt):
    global ParameterFound
    global Start
    global Input
    ParameterFound = False
    ParameterFound2 = False
    lower_case = prompt.lower()
    corrected = autocrct(lower_case, True)
    if lower_case != corrected:
        option = GetInput("Did you mean? " +corrected + " [y/n]:")
        if option.lower() == 'y' or option.lower() == 'yes' or option.lower() == 'yeah' or option.lower() == 'ya':
            lower_case = corrected
    if lower_case.find("search ") == 0 or lower_case.find("find ") == 0 or lower_case.find("fact ") == 0:
        if lower_case.find("search ") == 0:
            Print(Fact(lower_case[7:]))
        else:
            Print(Fact(lower_case[5:]))
    elif 'defin' in lower_case or 'meaning' in lower_case:
        tokens = word_tokenize(lower_case)
        if len(tokens) == 1:
            word = GetInput("What word would you like to define: ")
            word_to_define = word_tokenize(word)[0]
        else:
            if len(tokens) != 2:
                stopWords = set(stopwords.words("english"))
                stopWords.add('is')
                for a in tokens:
                    if a in stopWords:
                        tokens.remove(a)
            for b in tokens:
                if 'defin' not in b or 'meaning' not in b:
                    word_to_define = b
        try:
            Print(definition(word_to_define))
            Print("synonyms")
            Print(synonym(word_to_define))
            Print("antonyms")
            Print(antonym(word_to_define))
        except Exception:
            Print("That word does not seem to exist")
    elif 'timer' in lower_case or 'remind' in lower_case:
        tokens = word_tokenize(lower_case)
        for i in range(len(tokens)):
            if 'sec' in tokens[i]:
                if isInt(tokens[i-1]):
                    ParameterFound = True
                    seconds = int(tokens[i-1])
                    break
        activity_name = GetInput("What is the name of your activity:")
        while True:
            if ParameterFound:
                Print("The timer is starting it will last for " + str(seconds) + " seconds")
                Timer(seconds, activity_name, root)
                break
            try:
                seconds = int(GetInput("How many seconds do you want the timer for?"))
                Print("The timer is starting it will last for " + str(seconds) + " seconds")
                Timer(seconds, activity_name, root)
                break
            except Exception:
                Print("Please input an integer")
    elif 'time' in lower_case and not "sentiment" in lower_case:
        Print(time.ctime())
    elif 'news' in lower_case:
        Print(TopNews())
    elif 'shut down' in lower_case or 'power down' in lower_case or 'shut off' in lower_case or 'power off' in lower_case:
        tokens = word_tokenize(lower_case)
        for i in range(len(tokens)):
            if 'sec' in tokens[i]:
                if isInt(tokens[i-1]):
                    ParameterFound = True
                    seconds = int(tokens[i-1])
                    break
        while True:
            if ParameterFound:
                ShutDown(seconds)
                break
            try:
                seconds = int(GetInput("How many seconds do you want to shut down in?"))
                Print("The computer will shut down in " + seconds + " seconds")
                ShutDown(seconds)
                break
            except Exception:
                Print("Please input an integer")
    elif 'restart' in lower_case or 're-start' in lower_case or 're start' in lower_case:
        tokens = word_tokenize(lower_case)
        for i in range(len(tokens)):
            if 'sec' in tokens[i]:
                if isInt(tokens[i-1]):
                    ParameterFound = True
                    seconds = int(tokens[i-1])
                    break
        while True:
            if ParameterFound:
                Restart(seconds)
                break
            try:
                seconds = GetInput("How many seconds do you want to restart in?")
                Print("The computer will restart in " + seconds + " seconds")
                Restart(seconds)
                break
            except Exception:
                Print("Please input an integer")
    elif 'forecast' in lower_case:
        client = yweather.Client()
        WOEID = client.fetch_woeid('Singapore')
        Print(Forecast(WOEID))
    elif 'weather' in lower_case:
        client = yweather.Client()
        WOEID = client.fetch_woeid('Singapore')
        Print(CurrentWeather(WOEID))

    elif 'sing' in lower_case or 'play' in lower_case:
        while True:
            try:
                file = FileGet()
                Print(Music(file))
                break
            except Exception:
                Print("Your file may be corrupted")
    elif 'stop' in lower_case:
        StopMusic()
    elif 'create' in lower_case and 'list' in lower_case:
        tokens = word_tokenize()
        for i in range(len(tokens)):
            if 'list' in tokens[i] and i != tokens[i] - 1:
                ParameterFound = True
                list_name = tokens[i + 1]
                break
        if not ParameterFound:
            list_name = GetInput("What is the name for your list?")
            CreateList(list_name)
            Print("List successfully created")
        else:
            CreateList(list_name)
            Print("List successfully created")
    elif 'add' in lower_case and 'list' in lower_case or 'append' in lower_case and 'list' in lower_case:
        tokens = word_tokenize()
        for i in range(len(tokens)):
            if 'list' in tokens[i] and i != tokens[i] - 1 or 'to' in tokens[i] and i != tokens[i] - 1:
                ParameterFound = True
                list_name = tokens[i + 1]
                break
            elif 'add' in tokens[i] or 'append' in tokens[i]:
                ParameterFound2 = True
                AddToFile = tokens[i + 1]
                break
        if not ParameterFound:
            List_name = GetInput("Which list would you like to add to?")
        if not ParameterFound2:
            AddToFile = GetInput("What would you like to add to your list?")
        Print(AddList(List_name, AddToFile))
    elif 'remove' in lower_case and 'list' in lower_case or 'delete' in lower_case and 'list' in lower_case:
        tokens = word_tokenize()
        for i in range(len(tokens)):
            if 'list' in tokens[i] and i != tokens[i] - 1 or 'from' in tokens[i] and i != tokens[i] - 1:
                ParameterFound = True
                list_name = tokens[i + 1]
                break
            elif 'remove' in tokens[i] or 'delete' in tokens[i]:
                ParameterFound2 = True
                RemoveFromFile = tokens[i + 1]
                break
        if not ParameterFound:            
            List_name = GetInput("which list would you like to remove from?")
        if not ParameterFound2:
            RemoveFromFile = GetInput("What would you like to remove from your list?")
        Print(removeList(List_name, RemovefromFile))
    elif 'get' in lower_case and 'list' in lower_case or 'see' in lower_case and 'list' in lower_case:
        tokens = word_tokenize()
        for i in range(len(tokens)):
            if 'list' in tokens[i] and i != tokens[i] - 1:
                ParameterFound = True
                List_name = tokens[i + 1]
                break
        if not ParameterFound:
            List_name = GetInput("Which list would you like to see")
        Print(GetList(List_name))
    elif 'calc' in lower_case or 'evalu' in lower_case:
        tokens = lower_case.split(" ")
        for i in tokens:
            if isEqua(i):
                ParameterFound = True
                Equation = i
                break
        while True:
            if ParameterFound:
                Print(cal(Equation))
                break
            try:
                Equation = GetInput("Enter your formula:")
                if not isEqua(Equation):
                    int('')
                Print(cal(Equation))
                break
            except Exception:
                Print("Please input a valid equation")
    elif 'clean' in lower_case:
        Print("Choose the .csv file")
        file = FileGet()
        column = GetInput("What is the name of the column that you want to clean?")
        Print("Choose the .csv file you wish to load the data")
        file2 = FileGet()
        Print(ExtractRubbish(file, file2, column))
    elif 'extract int' in lower_case or 'get numbers' in lower_case:
        Print("Choose the .csv file")
        file = FileGet()
        column = GetInput("What is the name of the column that you want to extract integers from?")
        column2 = GetInput("What is the name of the column that you want place the new values?")
        Print(str(ExtractInts(file, column, column2)))
    elif 'positivity' in lower_case or 'sentiment' in lower_case:
        Print("Choose the .csv file")
        file = FileGet()
        column = GetInput("What is the name of the column that you want to extract sentiment from?")
        column2 = GetInput("What is the name of the column that you want place the new values?")
        Print(str(ExtractSentiment(file, column, column2)))
    elif 'topic' in lower_case:
        Print("Choose the .csv file")
        file = FileGet()
        column = GetInput("What is the name of the column that you want to extract topics from?")
        column2 = GetInput("What is the name of the column that you want place the new values?")
        Print(str(ExtractTopic(file, column, column2)))
    elif 'scatter plot' in lower_case:
        Print("Choose the .csv file")
        file = FileGet()
        column = GetInput("What is the name of the column that you want to extract data for the x axis?")
        column2 = GetInput("What is the name of the column that you want to extract data for the y axis?")
        Print(PlotScatterData(file, column, column2))
    elif 'line graph' in lower_case:
        Print("Choose the .csv file")
        file = FileGet()
        column = GetInput("What is the name of the column that you want to extract data for the x axis?")
        column2 = GetInput("What is the name of the column that you want to extract data for the y axis?")
        Print(PlotGraphData(file, column, column2))
    elif 'pie chart' in lower_case:
        Print("Choose the .csv file")
        file = FileGet()
        column = GetInput("What is the name of the column that you want to extract data?")
        labels = GetInput("Enter the labels seperated by commas")
        try:
            Print(PlotPieData(file, column, listFromStr(column2)))
        except Exception:
            Print("You inputted too many values")
    elif 'graph' in lower_case:
        tokens = lower_case.split(" ")
        for i in range(len(tokens)):
            if isFormula(tokens[i]):
                ParameterFound = True
                formula = tokens[i]
                break
        while True:
            if ParameterFound:
                graph(formula, -450, 460, t)
                break
            try:
                formula = GetInput("Enter your formula:")
                if not isFormula(formula):
                    int('')
                try:
                    graph(formula, -350, 360, t)
                    Print("Graphed " + formula)
                except Exception:
                    Print("Oops That formula is in the complex plane")
                break
            except Exception:
                Print("Please input a graphable formula")
    elif 'summar' in lower_case:
        tokens = word_tokenize(lower_case)
        parameter = 0
        for i in tokens:
            if 'web' in i:
                parameter = 1
                break
            elif 'text' in i or 'txt' in i:
                parameter = 2
                break
        if parameter == 0:
            WebText = GetInput("Do you want to summarise text files or websites?")
            while True:
                if 'web' in WebText:
                    parameter = 1
                    break
                elif 'text' in WebText or 'txt' in WebText:
                    parameter = 2
                    break
                else:
                    Print("You did not specify the type")
        if parameter == 1:
            while True:
                url = GetInput("What website do you want to summarise")
                if isUrl(url):
                    break
                else:
                    Print("That is not a valid url. Please use https: or www")
            Print(WebSummary(url))
        elif parameter == 2:
            Print("Which text file would you like to view")
            file = FileGet()
            Print(TextSummary(file))
    elif 'simplify' in lower_case:
        tokens = lower_case.split(" ")
        for i in tokens:
            if isEqua(i):
                ParameterFound = True
                Equation = i
                break
        while True:
            if ParameterFound:
                Print(simplifyEqu(Equation))
                break
            try:
                Equation = GetInput("Enter your equation:")
                if not isEqua(Equation):
                    int('')
                Print(simplifyEqu(Equation))
                break
            except Exception:
                Print("Please input a valid equation")
    elif 'expand' in lower_case:
        tokens = lower_case.split(" ")
        for i in tokens:
            if isEqua(i):
                ParameterFound = True
                Equation = i
                break
        while True:
            if ParameterFound:
                Print(expandEqu(Equation))
                break
            try:
                Equation = GetInput("Enter your equation:")
                if not isEqua(Equation):
                    int('')
                Print(expandEqu(Equation))
                break
            except Exception:
                Print("Please input a valid equation")
    elif 'factorise' in lower_case:
        tokens = lower_case.split(" ")
        for i in tokens:
            if isEqua(i):
                ParameterFound = True
                Equation = i
                break
        while True:
            if ParameterFound:
                Print(factoriseEqu(Equation))
                break
            try:
                Equation = GetInput("Enter your equation:")
                if not isEqua(Equation):
                    int('')
                Print(factoriseEqu(Equation))
                break
            except Exception:
                Print("Please input a valid equation")
    elif 'solve' in lower_case or 'find' in lower_case:
        tokens = lower_case.split(" ")
        for i in range(len(tokens)):
            if isFormula(tokens[i]):
                ParameterFound = True
                formula = tokens[i]
                break
        while True:
            try:
                if not ParameterFound:
                    formula = GetInput("Enter your formula:")
                if not isFormula(formula):
                    int('')
                subject = GetInput("Enter what you are solving for:")
                for i in solveEqu(formula.split("=")[0], formula.split("=")[1], subject, True):
                    Print(i)
                break
            except Exception:
                Print("Please input a valid subject")
    elif 'derivative' in lower_case or 'differentiate' in lower_case:
        tokens = lower_case.split(" ")
        for i in range(len(tokens)):
            if isEqua(tokens[i]):
                ParameterFound = True
                formula = tokens[i]
                break
        while True:
            try:
                if not ParameterFound:
                    formula = GetInput("Enter your formula:")
                if not isEqua(formula):
                    int('')
                subject = GetInput("Enter what you are solving for:")
                Print(diffCal(formula, subject))
                break
            except Exception:
                Print("Please input a valid subject")
    elif 'integrate' in lower_case:
        tokens = lower_case.split(" ")
        for i in range(len(tokens)):
            if isEqua(tokens[i]):
                ParameterFound = True
                formula = tokens[i]
                break
        while True:
            try:
                if not ParameterFound:
                    formula = GetInput("Enter your formula:")
                if not isEqua(formula):
                    int('')
                subject = GetInput("Enter what you are solving for:")
                try:
                    Print(str(integrateCal(formula, subject)) + " + C")
                except Exception:
                    Print("Sorry you cannot integrated that :(")
                break
            except Exception:
                Print("Please input a valid subject")
    elif 'convert' in lower_case:
        tokens = word_tokenize(lower_case)
        for i in range(len(tokens)):
            if isInt(tokens[i]):
                ParameterFound = True
                num = tokens[i]
                unit = tokens[i+1]
                break
            if tokens[i] == 'to':
                ParameterFound2 = True
                unit2 = tokens[i+1]
        while True:
            try:
                if not ParameterFound:
                    num = GetInput("Enter your number:")
                    unit = GetInput("Enter your first unit:")
                if not ParameterFound2:
                    unit2 = GetInput("Enter the unit you will convert to:")
                Print(UnitConvert(int(num), unit, unit2))
                break
            except Exception:
                Print("Please input a valid unit")
    Start = True
            
def Print(Text):
    Conversation.config(state=NORMAL)
    Conversation.insert(END, Text, 'tag-left')
    Conversation.insert(END, "\n\n")

def InputSignal():
    global Start
    global Input
    Input = True
    var.set(1)
    if Start:
        Start = False
        Input = False
        var.set(0)
        Conversation.config(state=NORMAL)
        Conversation.insert(END, TextBox.get(), 'tag-right')
        Conversation.insert(END, "\n\n")
        solve(TextBox.get())
        pass

def InputSignal2(event):
    global Start
    global Input
    Input = True
    var.set(1)
    if Start:
        Start = False
        Input = False
        var.set(0)
        Conversation.config(state=NORMAL)
        Conversation.insert(END, event.widget.get(), 'tag-right')
        Conversation.insert(END, "\n\n")
        solve(event.widget.get())
        pass

def listFromStr(strlist):
    return strlist.split(',')

def Clear():
    t.clear()
    gridX(20, t)
    gridY(20, t)
root = Tk()
root.overrideredirect(True)
width = root.winfo_screenwidth()
height = root.winfo_screenheight()
root.geometry('%dx%d+%d+%d' % (width*0.8, height*0.8, width*0.1, height*0.1))
image_file = "Logo.gif"
image = PhotoImage(file=image_file)
canvas = Canvas(root, height=height*0.8, width=width*0.8, bg="black")
canvas.create_image(width*0.8/2, height*0.8/2, image=image)
canvas.pack()
root.after(5000, root.destroy)
root.mainloop()
#Real Program
root = Tk()
root.title("Coeus")
w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry("%dx%d+0+0" % (w, h))
root.state("zoomed")
var = IntVar()
BoxText = StringVar()
var.set(0)
tabControl = ttk.Notebook(root)
Main = Frame(tabControl)
Help = Frame(tabControl)
tabControl.add(Main, text='Chat')
tabControl.add(Help, text='Help')
tabControl.pack(expand=1, fill="both")
imgicon = PhotoImage(file='Logo2.gif')
root.tk.call('wm', 'iconphoto', root._w, imgicon)
CanvaFrame = Frame(Main)
CanvaFrame.pack(side=RIGHT, padx=20)
canvas = Canvas(CanvaFrame, width = 700, height = 700, bg="white")
t = RawTurtle(canvas)
canvas.pack(pady=20)
S = Scrollbar(Main)
S.pack(side=RIGHT, fill=Y)
Conversation = Text(Main, wrap=WORD)
Conversation.pack(fill=Y, pady=20)
Conversation.config(yscrollcommand=S.set)
Conversation.config(state=DISABLED)
Conversation.tag_configure('tag-right', justify='right', foreground="seagreen")
Conversation.tag_configure('tag-left', justify='left', foreground="blue")
Sender = Frame(Main)
Sender.pack()
ButtonSend = Button(Sender, text= 'Send', command=InputSignal)
TextBox = Entry(Sender, width=90, textvariable=BoxText)
TextBox.bind('<Return>', InputSignal2)
TextBox.pack(side=LEFT, padx=10)
ButtonSend.pack(side=LEFT, padx=10)
ButtonRec = Button(Sender, text= 'Rec.', command=SpeechReg)
ButtonRec.pack(side=LEFT, padx=10)
Commands = Frame(Main)
Commands.pack(pady=20)
ComLabel = Label(Commands, text="Commands")
ComLabel.pack()
TClear = Button(Commands, text="Clear Shapes", command=Clear)
TClear.pack()
gridX(20, t)
gridY(20, t)
HelpText = Text(Help, wrap=WORD, height=100, width=100)
HelpText.pack()
HelpText.insert(END, 'Coeus is a ChatBased reasearch development environment.\n\n===Goal Of The App===\nThe goal of the app is to make it easier for people to research in a easier and less complex way,\nIt is mainly helpful for secondary research, primary data analysis(from surveys etc.) and mathematical functions needed for\ndevelopment of research.\n\n===Functions===\n1.Defining or meaning of word\n\tThis is self explanatory. To find the definition of a word. simply type "definition of <word>", "definition <word>", "meaning of <word>" or \n\t"meaning <word>". You can also type varients. You can also type just "define" and it will ask you for the word you want to define. This will \n\thelp you quickly define words for any part of your project\n\n2.Fact algorithm\n\tThis algorithm created by our team will find an answer to your query as best as it can. This algorithm was completely developed by are team\n\tand the hardest part of the app to create. To search and answer to a query simply type "search <query>" i.e "search height of burj khalifa".\n\tThis will make the research proccess a tad bit easier\n\n3.timer\n\tThis can set a timer for a certain amount of seconds and will alert you with os notifications after the specfic amount of seconds. simply\n\ttype "timer" or "timer for <certainNumberOfSeconds> seconds". This will help you manage your work and your breaks\n\n4.time\n\tJust type "time" to get the current time\n\n5.news\n\tType \'news\' to get the current international news. Which you may need to use for research\n\n6.shut down and restart\n\tSimply type "restart in <certainNumberOfSeconds> seconds" or "shut down in <certainNumberOfSeconds> seconds". This is a quick way to escape\n\tany program if it is creating errors that are affecting your computer\n\n7.forecast\n\tType "forecast" to get the forecast for the next few days of weather\n\n8.weather\n\tType "weather" to get the current weather for the day\n\n9.starting and stoping audio\n\tIf you would like to quickly listen to a voice recording(for interview etc.) all you have to type is "play" to open a file directory \n\tand play the song. Then if you would like to stop simply type "stop"\n\n==List functions==\nThis functions create lists, add items to lists, remove items from lists and view list.These Lists are stored on storage not RAM so if you close the \nprogram and re-open the program the list data will still be there. the list function can be used to manage tasks that you can do for a day\n\n10.Create List\n\tType "create list <name>".You can also type "create list" to create a list and it will ask you what you want to name it\n\n11.Add to List\n\tType "add to list" and it will ask you for the list name and the thing you want to add to the list\n\n12.Remove from List\n\tType "remove from list" and it will ask you for the list name and the thing you want to remove from the list\n\n13.Get list\n\tType "get list <name>" or "see list <name>" to see the list\n===csv functions===\nThese functions are used to maniputlate csv files for data analysis.\n\n14.Profanity Filter\n\tType "clean". This function removes profanity in a csv file\n\n15.Number Extract\n\tType "extract integers" or "get numbers". It gets numbers from a csv file\n\n16.Sentiment Extract\n\tType "extract sentiment". This function will help you extract sentiment from a chosen csv file\n\n17.topic\n\tType "topic" this will find the topic of a certain row or column of a csv file\n\n18.pie-chart\n\tType "pie chart" to get the pie chart of a two columns in a csv file\n\n19.line graph\n\tType "line graph" to get the line graph of a two columns in a csv file\n\n20.scatter-plot\n\ttype "scatter plot" to get the scatter plot of a two columns in a csv file\n\n===web and text functions===\n21.summary\n\tType "summary". It can take the summary of a web page or a text file\n\n===math functions===\t\n22.calculator\n\tcalculates equation. Type "calculate <equation>"(make sure the equation has no spaces in between in it) i.e "calculate 2^2"\n\t\n23.graph\n\tgraphs equation. Type "graph <equation>"(make sure the equation has no spaces in between in it) i.e "graph y=x^2"\n\t\n24.simplify\n\tType "simplify <equation>"(make sure the equation has no spaces in between in it) to simplify an equation\n\t\n25.factorise\n\tType "factorise <equation>"(make sure the equation has no spaces in between in it) to factorise an equation\n\t\n26.expand\n\tType "expand <equation>"(make sure the equation has no spaces in between in it) to expand an equation\n\t\n27.solve\n\tType "solve <equation>"(make sure the equation has no spaces in between in it) to solve a one variable algebra equation\n')
root.mainloop()
