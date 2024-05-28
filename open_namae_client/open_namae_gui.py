#!/usr/bin/env python3
# coding: utf-8


import tkinter as tk
from tkinter import font
from tkinter import messagebox
import os
import platform
import json
import webbrowser

import open_namae


APP_LICENSE_TEXT = "このアプリケーションは無権利創作宣言に準拠して著作権放棄されています"
APP_LICENSE_URL = "https://www.2pd.jp/license/"
APP_REPOSITORY_URL = "https://fossil.2pd.jp/open_namae_client/"


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
        "ip_address_api" : "http://api.example.jp/",
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
    global label_execution_status
    global entry_onamae_id
    global entry_password
    global entry_ip_address_api
    global entry_dns_host
    global entry_dns_port
    global domains_area
    
    main_win = tk.Tk()
    
    main_win.title(open_namae.APP_NAME + " コントロールパネル v" + open_namae.APP_VERSION)
    main_win.geometry("480x480")
    main_win.resizable(0, 0)
    main_win.configure(bg="#ffffff")
    
    main_win.protocol("WM_DELETE_WINDOW", close_main_window)
    
    main_menu = tk.Menu(main_win, bg="#eeeeee", activebackground="#ffffff", relief="flat")
    main_win.configure(menu=main_menu)
    
    if is_windows:
        main_win.iconbitmap("files/icon.ico")
        
        main_menu_file = tk.Menu(main_menu, tearoff=False, activebackground="#ffffff")
        main_menu_execution = tk.Menu(main_menu, tearoff=False, activebackground="#ffffff")
        main_menu_help = tk.Menu(main_menu, tearoff=False, activebackground="#ffffff")
        
        status_font = tk.font.Font(family="Yu Gothic", size=12)
        label_font = tk.font.Font(family="Yu Gothic", size=11)
        entry_font = tk.font.Font(family="Yu Gothic", size=10)
    else:
        main_win.iconphoto(True, tk.PhotoImage(file="files/icon.png"))
        
        main_menu_file = tk.Menu(main_menu, tearoff=False, bg="#eeeeee", activebackground="#ffffff", bd=10, relief="flat")
        main_menu_execution = tk.Menu(main_menu, tearoff=False, bg="#eeeeee", activebackground="#ffffff", bd=10, relief="flat")
        main_menu_help = tk.Menu(main_menu, tearoff=False, bg="#eeeeee", activebackground="#ffffff", bd=10, relief="flat")
        
        status_font = tk.font.Font(size=11)
        label_font = tk.font.Font(size=10)
        entry_font = tk.font.Font(size=9)
    
    main_menu.add_cascade(label="ファイル", menu=main_menu_file)
    main_menu_file.add_command(label="変更を適用", command=save_config, font=("",10))
    main_menu_file.insert_separator(1)
    main_menu_file.add_command(label="終了", command=close_main_window, font=("",10))
    
    main_menu.add_cascade(label="実行とログ", menu=main_menu_execution)
    main_menu_execution.add_command(label="この設定でDNS情報を更新", command=dns_update, font=("",10))
    main_menu_execution.add_command(label="最終実行ログ", command=show_last_execution_log, font=("",10))
    
    main_menu.add_cascade(label="ヘルプ", menu=main_menu_help)
    main_menu_help.add_command(label="ヘルプを開く", font=("",10), command=open_help_file)
    main_menu_help.insert_separator(1)
    main_menu_help.add_command(label="バージョン情報", font=("",10), command=open_app_info)
    
    label_execution_status = tk.Label(main_win, font=status_font, fg="#33bbdd", bg="#ffffff")
    label_execution_status.place(x=0, y=10, width=480, height=40)
    
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
    
    dns_update_button = tk.Button(main_win, text="この設定でDNS情報を更新", font=entry_font, command=dns_update, fg="#ffffff", bg="#33bbdd", relief="flat", highlightbackground="#33bbdd", activeforeground="#ffffff", activebackground="#aaeeff")
    dns_update_button.place(x=70, y=420, width=200, height=40)
    
    save_button = tk.Button(main_win, text="変更を適用", font=entry_font, command=save_config, fg="#ffffff", bg="#33bbdd", relief="flat", highlightbackground="#33bbdd", activeforeground="#ffffff", activebackground="#aaeeff")
    save_button.place(x=290, y=420, width=120, height=40)
    
    repeat_check_log()
    
    main_win.mainloop()


def close_main_window ():
    global config
    global main_win
    
    if messagebox.askokcancel(open_namae.APP_NAME , open_namae.APP_NAME + "の設定を終了しますか？"):
        main_win.destroy()


last_execution_log_mtime = None

def check_log ():
    global last_execution_log_mtime
    global label_execution_status
    
    log_file_name = "last_execution_log.json"
    
    error_occurred = False
    
    if os.path.isfile(log_file_name):
        log_file_mtime = os.path.getmtime(log_file_name)
        
        if last_execution_log_mtime == None or log_file_mtime > last_execution_log_mtime:
            last_execution_log_mtime = log_file_mtime
            
            try:
                with open(log_file_name, "r", encoding="utf-8") as log_fp:
                    log_data = json.load(log_fp)
                
                if log_data["execution_succeeded"]:
                    label_text = "DNS情報は " + log_data["execution_datetime"] + " に更新されました"
                else:
                    error_occurred = True
                    label_text = log_data["execution_datetime"] + " にDNS情報の更新でエラーが発生しました"
            except:
                error_occurred = True
                label_text = "ログファイルが読み込めません"
        else:
            return
    else:
        error_occurred = True
        label_text = "DNS情報更新処理の実行履歴がありません"
    
    if error_occurred:
        label_execution_status["fg"] = "#ee3333"
        label_execution_status["text"] = "【!】" + label_text
    else:
        label_execution_status["fg"] = "#33bbdd"
        label_execution_status["text"] = label_text


def repeat_check_log ():
    global main_win
    
    check_log()
    
    main_win.after(60000, repeat_check_log)


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


def dns_update ():
    global config
    
    update_config()
    
    ddns_client = open_namae.ddns_client()
    
    if ddns_client.get_global_ip_address(config["ip_address_api"]):
        if not ddns_client.update_dns_records(config["dns_host"], config["dns_port"], config["onamae_id"], config["password"], config["domains"]):
            messagebox.showerror(open_namae.APP_NAME ,"DNS情報の更新に失敗しました")
    else:
        messagebox.showerror(open_namae.APP_NAME ,"グローバルIPアドレスの取得に失敗しました")
    
    ddns_client.save_log()
    
    check_log()
    
    messagebox.showinfo(open_namae.APP_NAME ,"DNS情報の更新が終了しました")


def save_config ():
    global config
    
    update_config()
    
    with open("config.json", "w", encoding="utf-8") as json_fp:
        json.dump(config, json_fp, ensure_ascii=False, indent=4)
    
    messagebox.showinfo(open_namae.APP_NAME ,"設定を保存しました")


log_win = None

def show_last_execution_log ():
    global log_win
    global is_windows
    
    if log_win != None and log_win.winfo_exists():
        return
    
    log_win = tk.Toplevel()
    
    log_win.title("DNS情報更新ログ - " + open_namae.APP_NAME)
    log_win.geometry("640x480")
    log_win.resizable(0, 0)
    log_win.configure(bg="#ffffff")
    
    log_win.protocol("WM_DELETE_WINDOW", close_log)
    
    if is_windows:
        title_font = tk.font.Font(family="Yu Gothic", size=12)
        label_font = tk.font.Font(family="Yu Gothic", size=10)
        entry_font = tk.font.Font(family="Yu Gothic", size=11)
    else:
        title_font = tk.font.Font(size=11)
        label_font = tk.font.Font(size=10)
        entry_font = tk.font.Font(size=10)
    
    log_file_name = "last_execution_log.json"
    
    if os.path.isfile(log_file_name):
        try:
            with open(log_file_name, "r", encoding="utf-8") as log_fp:
                log_data = json.load(log_fp)
        except:
            log_data = None
    else:
        log_data = None
    
    label_title = tk.Label(log_win, text="DNS情報更新ログ", font=title_font, fg="#333333", bg="#ffffff")
    label_title.place(x=20, y=10, width=600, height=40)
    
    label_datetime = tk.Label(log_win, font=label_font, fg="#333333", bg="#ffffff")
    label_datetime.place(x=10, y=50)
    
    label_succeeded = tk.Label(log_win, font=label_font, fg="#333333", bg="#ffffff")
    label_succeeded.place(x=10, y=80)
    
    label_log = tk.Label(log_win, text="実行ログ", font=label_font, fg="#333333", bg="#ffffff")
    label_log.place(x=10, y=120)
    
    log_area_scroll_y = tk.Scrollbar(log_win, orient="vertical", bg="#eeeeee", activebackground="#ffffff")
    log_area = tk.Text(log_win, font=entry_font, fg="#333333", bg="#ffffff", padx=5, pady=5, relief="solid", yscrollcommand=log_area_scroll_y.set)
    log_area_scroll_y["command"] = log_area.yview
    log_area.place(x=15, y=150, width=595, height=310)
    log_area_scroll_y.place(x=610, y=150, width=15, height=310)
    
    if log_data != None:
        label_datetime["text"] = "実行日時: " + log_data["execution_datetime"]
        
        if log_data["execution_succeeded"]:
            label_succeeded["text"] = "実行結果: 成功"
        else:
            label_succeeded["text"] = "実行結果: 失敗"
        
        log_area.insert("1.0", log_data["log_text"])
    else:
        label_datetime["text"] = "DNS情報更新処理の実行履歴がありません"
    
    log_area["state"] = "disabled"


def close_log ():
    global log_win
    
    log_win.destroy()


def open_help_file():
    webbrowser.open("file://" + os.path.abspath("./README.html"))


app_info_win = None

def open_app_info ():
    global app_info_win
    global is_windows
    global icon_image
    
    if app_info_win != None and app_info_win.winfo_exists():
        return
    
    app_info_win = tk.Toplevel()
    
    app_info_win.title("バージョン情報 - " + open_namae.APP_NAME)
    app_info_win.geometry("480x240")
    app_info_win.resizable(0, 0)
    app_info_win.configure(bg="#ffffff")
    
    app_info_win.protocol("WM_DELETE_WINDOW", close_app_info)
    
    if is_windows:
        title_font = tk.font.Font(family="Yu Gothic", size=14)
        label_font = tk.font.Font(family="Yu Gothic", size=10)
        entry_font = tk.font.Font(family="Yu Gothic", size=11)
    else:
        title_font = tk.font.Font(size=14)
        label_font = tk.font.Font(size=10)
        entry_font = tk.font.Font(size=10)
    
    icon_image = tk.PhotoImage(file="files/icon.png")
    label_icon = tk.Label(app_info_win, image=icon_image, bg="#ffffff")
    label_icon.place(x=208, y=28)
    
    label_title = tk.Label(app_info_win, text=open_namae.APP_NAME + " v" + open_namae.APP_VERSION, font=title_font, fg="#333333", bg="#ffffff")
    label_title.place(x=0, y=100, width=480, height=40)
    
    label_license = tk.Label(app_info_win, text=APP_LICENSE_TEXT, font=label_font, fg="#666666", bg="#ffffff")
    label_license.place(x=0, y=140, width=480, height=30)
    
    button_open_license = tk.Button(app_info_win, text="ライセンス", font=entry_font, command=open_license_url, fg="#ffffff", bg="#33bbdd", relief="flat", highlightbackground="#33bbdd", activeforeground="#ffffff", activebackground="#aaeeff")
    button_open_license.place(x=90, y=180, width=140, height=30)
    
    button_open_repository = tk.Button(app_info_win, text="ソースコード", font=entry_font, command=open_repository_url, fg="#ffffff", bg="#33bbdd", relief="flat", highlightbackground="#33bbdd", activeforeground="#ffffff", activebackground="#aaeeff")
    button_open_repository.place(x=250, y=180, width=140, height=30)


def open_license_url ():
    webbrowser.open(APP_LICENSE_URL)


def open_repository_url ():
    webbrowser.open(APP_REPOSITORY_URL)


def close_app_info ():
    global app_info_win
    
    app_info_win.destroy()


open_main_window()
