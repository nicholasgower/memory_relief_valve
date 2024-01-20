# -*- coding: utf-8 -*-
"""
Created on Thu Jan 18 10:01:03 2024

@author: Nicholas
"""
from time import sleep
import psutil
import wmi
import configparser
import os
import platform
import tkinter as tk
from datetime import datetime
from PIL import Image
import pystray
import threading
import ctypes  # An included library with Python install.   
from windows_toasts import Toast, WindowsToaster

config=configparser.ConfigParser()
config_filename="config_memory_relief_valve.ini"

running_check=False
"""
class gui(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Memory Relief Valve")
        self.geometry('500x250')
        self.protocol("WM_DELETE_WINDOW",self.minimize_to_tray)
        self.ram_cutoff=float(config["DEFAULT"]["RAM_cutoff"])
        self.check_frequency=float(config['DEFAULT']["check_frequency"])
        
        self.update()
    def update(self):
        memory=psutil.virtual_memory()
        #print("{}: {}%/{}% RAM consumed.".format(datetime.now(),memory.percent,self.ram_cutoff))
        self.title("Memory Relief Valve({}%/{}%)".format(memory.percent,self.ram_cutoff))
        if memory.percent>=self.ram_cutoff:
            open_relief_valve()
            
        self.after(1000,self.update)
      
    def minimize_to_tray(self):
        self.withdraw()
        image= Image.open("img/relief-valve.png")
        
        menu = (pystray.MenuItem('Quit',  self.quit_window), 
               pystray.MenuItem('Show',self.show_window))
        self.icon = pystray.Icon("name", image, "My App", menu)
        #self.update()
        self.icon.notify("Memory Relief Valve is now in background.","Memory Relief Valve")
        self.updateThread=threading.Thread(target=self.icon.run)
        
        self.updateThread.start()
        self.update()
        
        
    def quit_window(self, icon):
        icon.stop()
        self.updateThread.join()
        self.destroy()

    def show_window(self, icon):
        icon.stop()
        self.after(0,self.deiconify)
"""    
        
        
def generate_config():
    new_config=configparser.ConfigParser()
    new_config['DEFAULT']={}
    new_config['DEFAULT']["RAM_cutoff"]=str(95) #Shut down processes when RAM usage exceeds 95%
    new_config['DEFAULT']["shutdown_processes"]="firefox.exe chrome.exe"
    new_config['DEFAULT']["check_frequency"]=str(1)
    with open(config_filename,"w") as file:
        new_config.write(file)
        
def get_sacrificial_processes() -> list[str]:
    with open("close_processes.txt","r") as file:
        return file.read().replace("\r\n","\n").split("\n")
    
def terminate_process(name="firefox.exe"):
    f= wmi.WMI()
    for process in psutil.process_iter():
        #print(process.name())
        if process.name() == name:
            #print(name)
            process.terminate()
        
            
def open_relief_valve():
    """ Terminate all processes defined in 'shutdown_processes.' Activated when memory usage exceeds trigger value."""
    #print()
    message_opened()
    for process in config["DEFAULT"]["shutdown_processes"].split(" "):
        terminate_process(process)
    sleep(60)        
def message_start():
    toaster = WindowsToaster('Memory Relief Valve')
    newToast = Toast()
    newToast.text_fields = ['Memory Relief Valve initialized']
    newToast.text_fields.append("Will trigger when RAM usage exceeds {}%".format(config["DEFAULT"]["RAM_cutoff"]))
    
        
    toaster.show_toast(newToast)     
def message_opened():
    toaster = WindowsToaster('Memory Relief Valve')
    newToast = Toast()
    newToast.text_fields = ['Memory Relief Valve opened due to low memory.']
    newToast.text_fields.append("Processes closed:")
    newToast.text_fields.append(config["DEFAULT"]["shutdown_processes"])
        
    toaster.show_toast(newToast)

class memory_manager:
    def __init__(self):
        self.run_update=True
        self.update()
    def update(self):
        while True:
            ram_cutoff=float(config["DEFAULT"]["RAM_cutoff"])
            #ram_cutoff=40.0
            check_frequency=float(config['DEFAULT']["check_frequency"])
            memory=psutil.virtual_memory()
            #print("{}: {}%/{}% RAM consumed.".format(datetime.now(),memory.percent,self.ram_cutoff))
            print("Memory Relief Valve({}%/{}%)".format(memory.percent,ram_cutoff))
            if memory.percent>=ram_cutoff:
                open_relief_valve()
                    
            sleep(1)
            

def main():

    if os.path.exists(config_filename):
    
        config.read(config_filename)
    else:
        print("Config not found. Generating new config at {}".format(config_filename))
        generate_config()
        config.read(config_filename)
    #for key in config:
        #print(key,config[key])
        
    message_start()
    manager=memory_manager()
    #window=gui()
    #window.mainloop()        




    
        
    
    
if __name__=="__main__":
    if platform.system() != 'Windows':
        raise OSError("This program is designed to run only on Windows.")
    else:
        main()