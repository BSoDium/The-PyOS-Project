from colorama import init as init_colorama
from colorama import Fore, Style
import sys,os
import urllib.request
from zipfile import ZipFile

URL = 'https://github.com/the-fancy-corporation/The-PyOS-Project/releases/download/0.9/PyOS.release.0.9.zip'
CWD = os.getcwd()
class app:
    def __init__(self):
        init_colorama()
        self.talking='setup manager'
        self.step_title('Welcome to the PyOS software installer')
        check=self.ask('Do you want to proceed ? (y/n)')
        if check=='y':
            try:
                import panda3d
                self.step_title('The panda3d library is already installed')
            except:
                self.step_title('Oops, it looks like the panda3d library is not available on your machine')
                check2=self.ask('Do you want to install it ? Doing so will allow you to run the code directly from the python IDE (y/n)')
            check1=self.ask("Do you want to download the last stable release ? It is recommended to do so if you're not a developer (y/n)")
            if check1=='y':
                try:
                    zipObject=ZipFile(CWD+'\\downloads\\update.zip','r')
                    self.step_title('Existing data file detected, loading data from'+CWD+'\\downloads\\update.zip'+'\nInitializing extraction\nExtracting, please wait...')
                except:
                    self.step_title('Download has started...')
                    self.step_title('Please be patient, the download speed depends on your internet connection.\nFile size is approximately 500Mb')
                    urllib.request.urlretrieve(URL,CWD+'\\downloads\\update.zip')
                    self.step_title('Download complete, initializing extraction\nExtracting, please wait...')
                    zipObject=ZipFile(CWD+'\\downloads\\update.zip','r')
                zipObject.extractall(CWD+'\\downloads')
                self.step_title('Extraction complete, files available at: '+CWD+'\\downloads')
                self.step_title('Deleting additionnal temporary files...')
                zipObject.close()
                os.remove(CWD+'\\downloads\\update.zip')
                self.step_title('Operation successful\nExiting installation program')
                input('press Enter to continue...')
        else:
            sys.exit(0)
    
    def color(self,string, col):
        return col + string + Style.RESET_ALL

    def step_title(self, title):
        print("\n\n[", self.talking.zfill(2), "] ", self.color(title, Fore.CYAN + Style.BRIGHT))
    
    def ask(self,content):
        print(self.color(content, Fore.YELLOW + Style.BRIGHT))
        return input('')

app()

