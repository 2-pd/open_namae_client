#!/usr/bin/env python3
# coding: utf-8


#
# LICENSE
#
#  このソフトウェアは、無権利創作宣言に基づき著作権放棄されています。
#  営利・非営利を問わず、自由にご利用いただくことが可能です。
#
#   https://www.2pd.jp/license/
#


import tkinter as tk
from tkinter import font
from tkinter import messagebox
import os
import platform
import json


APP_NAME = "Open NAMAE client"
APP_VERSION = "24.05-1"


app_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(app_dir)

if platform.system() == "Windows":
    is_windows = True
else:
    is_windows = False

default_dir = os.path.dirname(app_dir)

try:
    with open("config.json", "r", encoding="utf-8") as json_fp:
        config = json.load(json_fp)
except:
    config = {
        "onamae_id" : "",
        "password" : "",
        "ip_address_api" : "http://ifconfig.example.jp/",
        "dns_host" : "ddnsclient.onamae.com",
        "dns_port" : 65010,
        "domains" : []
    }


def open_main_window ():
    global config
    global is_windows
    global main_win
    
    main_win = tk.Tk()
    
    main_win.title(APP_NAME + " v" + APP_VERSION)
    main_win.geometry("480x480")
    main_win.resizable(0, 0)
    main_win.configure(bg="#ffffff")
    
    main_win.protocol("WM_DELETE_WINDOW", close_main_window)
    
    if is_windows:
        main_win.iconbitmap("files/icon.ico")
        
        label_font = tk.font.Font(family="Yu Gothic", size=12)
        button_font = tk.font.Font(family="Yu Gothic", size=11)
    else:
        main_win.iconphoto(True, tk.PhotoImage(file="files/icon.png"))
        
        label_font = tk.font.Font(size=12)
        button_font = tk.font.Font(size=10)
    
    main_win.mainloop()


def close_main_window ():
    global config
    global main_win
    
    with open("config.json", "w", encoding="utf-8") as json_fp:
        json.dump(config, json_fp, ensure_ascii=False, indent=4)
    
    main_win.destroy()


open_main_window()
