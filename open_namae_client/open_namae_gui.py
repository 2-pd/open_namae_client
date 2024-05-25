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
        "domains" : [
            {
                "domain_name" : "example1.jp"
            },
            {
                "host_name" : "www",
                "domain_name" : "example2.jp"
            }
        ]
    }


def open_main_window ():
    global config
    global is_windows
    global main_win
    global entry_onamae_id
    global entry_password
    global entry_ip_address_api
    global entry_dns_host
    global entry_dns_port
    global domains_area
    
    main_win = tk.Tk()
    
    main_win.title(APP_NAME + " コントロールパネル v" + APP_VERSION)
    main_win.geometry("480x480")
    main_win.resizable(0, 0)
    main_win.configure(bg="#ffffff")
    
    main_win.protocol("WM_DELETE_WINDOW", close_main_window)
    
    if is_windows:
        main_win.iconbitmap("files/icon.ico")
        
        label_font = tk.font.Font(family="Yu Gothic", size=11)
        entry_font = tk.font.Font(family="Yu Gothic", size=10)
    else:
        main_win.iconphoto(True, tk.PhotoImage(file="files/icon.png"))
        
        label_font = tk.font.Font(size=10)
        entry_font = tk.font.Font(size=9)
    
    label_onamae_id = tk.Label(main_win, text="お名前ID:", font=label_font, fg="#333333", bg="#ffffff")
    label_onamae_id.place(x=10, y=60)
    
    entry_onamae_id = tk.Entry(main_win, width=20, font=entry_font, fg="#333333", bg="#ffffff", bd=1, relief="solid")
    entry_onamae_id.insert(0, config["onamae_id"])
    entry_onamae_id.place(x=75, y=60)
    
    label_password = tk.Label(main_win, text="パスワード:", font=label_font, fg="#333333", bg="#ffffff")
    label_password.place(x=240, y=60)
    
    entry_password = tk.Entry(main_win, show="*", width=20, font=entry_font, fg="#333333", bg="#ffffff", bd=1, relief="solid")
    entry_password.insert(0, config["password"])
    entry_password.place(x=315, y=60)
    
    label_ip_address_api = tk.Label(main_win, text="グローバルIP確認URL:", font=label_font, fg="#333333", bg="#ffffff")
    label_ip_address_api.place(x=10, y=100)
    
    entry_ip_address_api = tk.Entry(main_win, width=40, font=entry_font, fg="#333333", bg="#ffffff", bd=1, relief="solid")
    entry_ip_address_api.insert(0, config["ip_address_api"])
    entry_ip_address_api.place(x=155, y=100)
    
    label_dns_host = tk.Label(main_win, text="DDNSホスト:", font=label_font, fg="#333333", bg="#ffffff")
    label_dns_host.place(x=10, y=140)
    
    entry_dns_host = tk.Entry(main_win, width=25, font=entry_font, fg="#333333", bg="#ffffff", bd=1, relief="solid")
    entry_dns_host.insert(0, config["dns_host"])
    entry_dns_host.place(x=100, y=140)
    
    label_dns_port = tk.Label(main_win, text="DDNSポート:", font=label_font, fg="#333333", bg="#ffffff")
    label_dns_port.place(x=290, y=140)
    
    entry_dns_port = tk.Entry(main_win, width=10, font=entry_font, fg="#333333", bg="#ffffff", bd=1, relief="solid")
    entry_dns_port.insert(0, config["dns_port"])
    entry_dns_port.place(x=380, y=140)
    
    label_domains = tk.Label(main_win, text="ドメイン (ホスト名とドメイン名はセミコロンで区切って入力)", font=label_font, fg="#333333", bg="#ffffff")
    label_domains.place(x=10, y=190)
    
    domains_area_scroll_y = tk.Scrollbar(main_win, orient="vertical", bg="#eeeeee", activebackground="#ffffff")
    domains_area = tk.Text(main_win, font=entry_font, fg="#333333", bg="#ffffff", padx=5, pady=5, relief="solid", yscrollcommand=domains_area_scroll_y.set)
    domains_area_scroll_y["command"] = domains_area.yview
    domains_area.place(x=15, y=220, width=435, height=180)
    domains_area_scroll_y.place(x=450, y=220, width=15, height=180)
    
    for domain_data in config["domains"]:
        if "host_name" in domain_data:
            domains_area.insert(tk.END, domain_data["host_name"] + ";" + domain_data["domain_name"] + "\n")
        else:
            domains_area.insert(tk.END, domain_data["domain_name"] + "\n")
    
    dns_update_button = tk.Button(main_win, text="この設定でDNS情報を更新", font=entry_font, fg="#ffffff", bg="#33bbdd", relief="flat", highlightbackground="#33bbdd", activeforeground="#ffffff", activebackground="#aaeeff")
    dns_update_button.place(x=70, y=420, width=200, height=40)
    
    save_button = tk.Button(main_win, text="変更を適用", font=entry_font, command=save_config, fg="#ffffff", bg="#33bbdd", relief="flat", highlightbackground="#33bbdd", activeforeground="#ffffff", activebackground="#aaeeff")
    save_button.place(x=290, y=420, width=120, height=40)
    
    main_win.mainloop()


def close_main_window ():
    global config
    global main_win
    
    if messagebox.askokcancel(APP_NAME , APP_NAME + "の設定を終了しますか？"):
        main_win.destroy()


def update_config ():
    global config
    global entry_onamae_id
    global entry_password
    global entry_ip_address_api
    global entry_dns_host
    global entry_dns_port
    global domains_area
    
    config["onamae_id"] = entry_onamae_id.get()
    config["password"] = entry_password.get()
    config["ip_address_api"] = entry_ip_address_api.get()
    config["dns_host"] = entry_dns_host.get()
    config["dns_port"] = int(entry_dns_port.get())
    
    config["domains"] = []
    domains = domains_area.get("1.0", tk.END).split()
    for domain_str in domains:
        domain_str = domain_str.strip()
        
        if len(domain_str) == 0:
            continue
        
        domain_data = domain_str.split(";")
        
        if len(domain_data) == 1:
            config["domains"].append({
                "domain_name" : domain_str
            })
        else:
            config["domains"].append({
                "host_name" : domain_data[0].strip(),
                "domain_name" : domain_data[-1].strip()
            })


def save_config ():
    global config
    
    update_config()
    
    with open("config.json", "w", encoding="utf-8") as json_fp:
        json.dump(config, json_fp, ensure_ascii=False, indent=4)
    
    messagebox.showinfo(APP_NAME ,"設定を保存しました")


open_main_window()
