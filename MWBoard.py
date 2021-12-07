import pyttsx3
import tkinter as tk
from tkinter import ttk
import time
from time import sleep
import os
key = tk.Tk()

String = " "

def press(num):
    global String
    String=String + str(num)
    equation.set(String)
    file = open("voice_file.txt","w+")
    file.readline()
    file.write(String)
    file.close()

def clear():
    global String
    String = " "
    equation.set(String)


def Voice():
    file = open("voice_file.txt","r")
    data = file.read()
    file.close()
    engine = pyttsx3.init() # object creation

    """ RATE"""
    rate = engine.getProperty('rate')   # getting details of current speaking rate
    engine.setProperty('rate', 150)     # setting up new voice rate

    """VOLUME"""
    volume = engine.getProperty('volume')   #getting to know current volume level (min=0 and max=1)
    engine.setProperty('volume',1.0)    # setting up volume level  between 0 and 1

    """VOICE"""
    voices = engine.getProperty('voices')       #getting details of current voice
    #engine.setProperty('voice', voices[0].id)  #changing index, changes voices. o for male
    engine.setProperty('voice', voices[1].id)   #changing index, changes voices. 1 for female

    engine.say(data)
    engine.runAndWait()
    engine.stop()


def action():
    String = " Next Line : "
    equation.set(String)


# Size window size
key.geometry('680x250')         # normal size 1010x250
key.maxsize(width=640, height=246)      # maximum size
key.minsize(width= 680 , height = 246)     # minimum size
# end window size

key.configure(bg = 'yellow')    #  add background color

# entry box
equation = tk.StringVar()
Dis_entry = ttk.Entry(key, state='readonly', font=('calibre', 12, 'normal'), textvariable=equation)
Dis_entry.grid(rowspan=1, columnspan=300, ipadx=999, ipady=10)

# font=('calibre',10,'normal')
n1 = ttk.Button(key, text='1', width=4, command=lambda: press('1'))
n1.grid(row=1, column=0, ipadx=6, ipady=10)

n1 = ttk.Button(key, text='2', width=4, command=lambda: press('2'))
n1.grid(row=1, column=1, ipadx=6, ipady=10)

n1 = ttk.Button(key, text='3', width=4, command=lambda: press('3'))
n1.grid(row=1, column=2, ipadx=6, ipady=10)

n1 = ttk.Button(key, text='4', width=4, command=lambda: press('4'))
n1.grid(row=1, column=3, ipadx=6, ipady=10)

n1 = ttk.Button(key, text='5', width=4, command=lambda: press('5'))
n1.grid(row=1, column=4, ipadx=6, ipady=10)

n1 = ttk.Button(key, text='6', width=4, command=lambda: press('6'))
n1.grid(row=1, column=5, ipadx=6, ipady=10)

n1 = ttk.Button(key, text='7', width=4, command=lambda: press('7'))
n1.grid(row=1, column=6, ipadx=6, ipady=10)

n1 = ttk.Button(key, text='8', width=4, command=lambda: press('8'))
n1.grid(row=1, column=7, ipadx=6, ipady=10)

n1 = ttk.Button(key, text='9', width=4, command=lambda: press('9'))
n1.grid(row=1, column=8, ipadx=6, ipady=10)

n1 = ttk.Button(key, text='0', width=4, command=lambda: press('0'))
n1.grid(row=1, column=9, ipadx=6, ipady=10)

back_slash = ttk.Button(key, text='Voice', width=4, command=Voice)
back_slash.grid(row=1, column=10, ipadx=20, ipady=10)


q = ttk.Button(key,text = 'Q' , width = 4, command = lambda : press('Q'))
q.grid(row = 2 , column = 0, ipadx = 6 , ipady = 10)

w = ttk.Button(key,text = 'W' , width = 4, command = lambda : press('W'))
w.grid(row = 2 , column = 1, ipadx = 6 , ipady = 10)

E = ttk.Button(key,text = 'E' , width = 4, command = lambda : press('E'))
E.grid(row = 2 , column = 2, ipadx = 6 , ipady = 10)

R = ttk.Button(key,text = 'R' , width = 4, command = lambda : press('R'))
R.grid(row = 2 , column = 3, ipadx = 6 , ipady = 10)

T = ttk.Button(key,text = 'T' , width = 4, command = lambda : press('T'))
T.grid(row = 2 , column = 4, ipadx = 6 , ipady = 10)

Y = ttk.Button(key,text = 'Y' , width = 4, command = lambda : press('Y'))
Y.grid(row = 2 , column = 5, ipadx = 6 , ipady = 10)

U = ttk.Button(key,text = 'U' , width = 4, command = lambda : press('U'))
U.grid(row = 2 , column = 6, ipadx = 6 , ipady = 10)

I = ttk.Button(key,text = 'I' , width = 4, command = lambda : press('I'))
I.grid(row = 2 , column = 7, ipadx = 6 , ipady = 10)

O = ttk.Button(key,text = 'O' , width = 4, command = lambda : press('O'))
O.grid(row = 2 , column = 8, ipadx = 6 , ipady = 10)

P = ttk.Button(key,text = 'P' , width = 4, command = lambda : press('P'))
P.grid(row = 2 , column = 9, ipadx = 6 , ipady = 10)

clear = ttk.Button(key,text = 'Clear' , width = 4, command = clear)
clear.grid(row = 2 , column = 10, ipadx = 19 , ipady = 10)



A = ttk.Button(key,text = 'A' , width = 4, command = lambda : press('A'))
A.grid(row = 3 , column = 0, ipadx = 6 , ipady = 10)

S = ttk.Button(key,text = 'S' , width = 4, command = lambda : press('S'))
S.grid(row = 3 , column = 1, ipadx = 6 , ipady = 10)

D = ttk.Button(key,text = 'D' , width = 4, command = lambda : press('D'))
D.grid(row = 3 , column = 2, ipadx = 6 , ipady = 10)

F = ttk.Button(key,text = 'F' , width = 4, command = lambda : press('F'))
F.grid(row = 3 , column = 3, ipadx = 6 , ipady = 10)

G = ttk.Button(key,text = 'G' , width = 4, command = lambda : press('G'))
G.grid(row = 3 , column = 4, ipadx = 6 , ipady = 10)

H = ttk.Button(key,text = 'H' , width = 4, command = lambda : press('H'))
H.grid(row = 3 , column = 5, ipadx = 6 , ipady = 10)

J = ttk.Button(key,text = 'J' , width = 4, command = lambda : press('J'))
J.grid(row = 3 , column = 6, ipadx = 6 , ipady = 10)

K = ttk.Button(key,text = 'K' , width = 4, command = lambda : press('K'))
K.grid(row = 3 , column = 7, ipadx = 6 , ipady = 10)

L = ttk.Button(key,text = 'L' , width = 4, command = lambda : press('L'))
L.grid(row = 3 , column = 8, ipadx = 6 , ipady = 10)

enter = ttk.Button(key,text = 'Enter' , width = 4, command = action)
enter.grid(row = 3, columnspan = 112, ipadx = 50 , ipady = 10)


Z = ttk.Button(key,text = 'Z' , width = 4, command = lambda : press('Z'))
Z.grid(row = 4 , column = 0, ipadx = 6 , ipady = 10)

X = ttk.Button(key,text = 'X' , width = 4, command = lambda : press('X'))
X.grid(row = 4 , column = 1, ipadx = 6 , ipady = 10)

C = ttk.Button(key,text = 'C' , width = 4, command = lambda : press('C'))
C.grid(row = 4 , column = 2, ipadx = 6 , ipady = 10)

V = ttk.Button(key,text = 'V' , width = 4, command = lambda : press('V'))
V.grid(row = 4 , column = 3, ipadx = 6 , ipady = 10)

B = ttk.Button(key, text= 'B' , width = 4 , command = lambda : press('B'))
B.grid(row = 4 , column = 4 , ipadx = 6 ,ipady = 10)

N = ttk.Button(key,text = 'N' , width = 4, command = lambda : press('N'))
N.grid(row = 4 , column = 5, ipadx = 6 , ipady = 10)

M = ttk.Button(key,text = 'M' , width = 4, command = lambda : press('M'))
M.grid(row = 4 , column = 6, ipadx = 6 , ipady = 10)

space = ttk.Button(key,text = 'Space' , width = 4, command = lambda : press(' '))
space.grid(row = 4 , columnspan = 89, ipadx = 108 , ipady = 10)

#dot = ttk.Button(key,text = '.' , width = 4, command = lambda : press('.'))
#dot.grid(row = 4 , column = 90, ipadx = 90 , ipady = 10)

key.mainloop()

