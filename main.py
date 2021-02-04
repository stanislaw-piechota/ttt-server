from requests import get
from tkinter import *
import json
import threading

root = Tk()
root.geometry('300x400+500+200')
root.config(bg='#ffffff')
root.resizable(False, False)

def checkMove():
    while True:
        text = get(f'https://najlepszawgalaktyce.000webhostapp.com/ttt/?move&check&code={code}').text
        print(text)
        data = json.loads(text)
        if data['move'] == num or data['win']:
            break

    try:
        if not data['win'] or data['win']=='t':
            if player: os[done].place(x=data['last'][1]*100+5, y=data['last'][0]*100+5, width=90, height=90)
            else: xs[done].place(x=data['last'][1]*100+5, y=data['last'][0]*100+5, width=90, height=90)
    except Exception as e:
        print(e)

    if not data['win']:
        stateLabel.config(text='Your move')
        for i in range(3):
            for j in range(3):
                if (i, j) not in data['board']:
                    fields[i][j].bind('<Button-1>', add)
    else:
        if data['win'] == 'x':
            if player: stateLabel.config(text='You won')
            else: stateLabel.config(text='You lost')
        elif data['win'] == 't':
            stateLabel.config(text='Tie')
        else:
            if player: stateLabel.config(text='You lost')
            else: stateLabel.config(text='You won')
def submit():
    global done
    done += 1
    data = get(f'https://najlepszawgalaktyce.000webhostapp.com/ttt/?move&x={x}&y={y}&code={code}')
    for i in range(3):
        for j in range(3):
            fields[i][j].unbind('<Button-1>')
    stateLabel.config(text='Wait for opponents move')
    waitThread = threading.Thread(target=checkMove); waitThread.start()
def add(event):
    global x, y
    if player: label = xs[done]
    else: label = os[done]
    label.place(x=event.widget.y*100+5, y=event.widget.x*100+5, width=90, height=90)
    x, y = event.widget.x, event.widget.y
    submit()
def checkStart():
    while True:
        data = json.loads(get(f'https://najlepszawgalaktyce.000webhostapp.com/ttt/?started&code={code}').text)
        if data['started']:
            break
    forgetWait()
    placeGame()
    stateLabel.config(text='Your move')
def create():
    global player, code, move, num
    text = get('https://najlepszawgalaktyce.000webhostapp.com/ttt/?create').text
    data = json.loads(text)
    code, player, move, num = data['code'], data['player'], True, 1

    checkThread = threading.Thread(target=checkStart); checkThread.start()

    codeLabel.config(text=f'Code: {code}'); forgetMenu(); placeWait()
    for i in range(3):
        for j in range(3):
            fields[i][j].bind('<Button-1>', add)
def join():
    global player, code, move, num
    code = codeInput.get().upper()
    text = get(f'https://najlepszawgalaktyce.000webhostapp.com/ttt/?join&code={code}').text
    data, move = json.loads(text), False
    player, num = data['player'], 2
    forgetCodeInput(); placeGame()
    stateLabel.config(text='Wait for opponents move')

    waitThread= threading.Thread(target=checkMove)
    waitThread.start()
def placeCodeInput():
    forgetMenu()
    codeInput.place(relx=0.3, rely=0.35, relwidth=0.4, relheight=0.1)
    codeSubmit.place(relx=0.4, rely=0.45, relwidth=0.2, relheight=0.1)
def forgetCodeInput():
    codeInput.place_forget()
    codeSubmit.place_forget()
def placeGame():
    for i in range(3):
        for j in range(3):
            fields[i][j].place(x=j*100, y=i*100, width=100, height=100)

    for i in range(2):
        board[i*2].place(x=(i+1)*100-0.5, y=0, width=1, height=300)
        board[i*2+1].place(x=0, y=(i+1)*100-0.5, width=300, height=1)
def forgetMenu():
    createButton.place_forget()
    joinButton.place_forget()
    #codeLabel.place_forget()
def placeMenu():
    createButton.place(x=100, y=65, width=100, height=50)
    joinButton.place(x=100, y=125, width=100, height=50)
    #codeLabel.place(x=100, y=185, width=100, height=25)
def placeWait():
    waitLabel.place(relx=0, rely=0.4, relwidth=1, relheight=0.1)
    codeLabel.place(relx=0, rely=0.5, relwidth=1, relheight=0.1)
def forgetWait():
    waitLabel.place_forget()
    codeLabel.place_forget()

fields = []
board = []
xs = []
os = []
player, num, code, move, done, x, y = None, 0, None, None, 0, 0, 0

boardFrame = Frame(bg='#ffffff')
stateLabel = Label(bg='white')
stateLabel.place(x=0, y=300, width=300, height=100)
waitLabel = Label(boardFrame, text='Waiting for opponent', bg='white')
codeInput = Entry(boardFrame, justify='center', bg='#efefef')
codeSubmit = Button(boardFrame, text='ENTER', bg='#dbdbdb', bd=0, command=join)

for i in range(3):
    fields.append([])
    for j in range(3):
        label = Label(boardFrame, bg='#ffffff'); fields[i].append(label)
        label.y = j; label.x = i
for i in range(1, 3):
    label = Label(boardFrame, bg='#000000'); board.append(label)
    label1 = Label(boardFrame, bg='#000000'); board.append(label1)
for i in range(5):
    canvas = Canvas(boardFrame, bg='white')
    canvas.create_line(0, 0, 90, 90)
    canvas.create_line(90, 0, 0, 90)
    xs.append(canvas)

    canvas = Canvas(boardFrame, bg='white')
    canvas.create_oval(5, 5, 85, 85)
    os.append(canvas)

createButton = Button(boardFrame, text='Create room', bg='#dbdbdb', fg='#000000', bd=0, command=create)
joinButton = Button(boardFrame, text='Join room', bg='#dbdbdb', bd=0, command=placeCodeInput)
codeLabel = Label(boardFrame, text='Code: ', bg='white')

placeMenu()
boardFrame.place(x=0, y=0, width=300, height=300)

root.mainloop()
