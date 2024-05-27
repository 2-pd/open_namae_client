# coding: utf-8

import os
import traceback
import urllib.request
import socket
import ssl
import json
import datetime


#
# LICENSE
#
#  このソフトウェアは、無権利創作宣言に基づき著作権放棄されています。
#  営利・非営利を問わず、自由にご利用いただくことが可能です。
#
#   https://www.2pd.jp/license/
#


APP_NAME = "Open NAMAE client"
APP_VERSION = "24.05-1"


class ddns_client:
    def __init__ (self):
        self.execution_datetime = str(datetime.datetime.today())[0:19]
        self.log_text = APP_NAME + " v" + APP_VERSION + "\n\n"
        self.global_ip_address = None
        self.execution_succeeded = True
    
    
    def add_log (self, log, is_error=False):
        if is_error:
            self.log_text += "【ERROR】 "
        
        self.log_text += log
    
    
    def save_log (self):
        log_file_path = os.path.dirname(os.path.abspath(__file__)) + "/last_execution_log.json"
        
        log_data = {
            "execution_succeeded" : self.execution_succeeded,
            "execution_datetime" : self.execution_datetime,
            "log_text" : self.log_text
        }
        
        try:
           with open(log_file_path, "w", encoding="utf-8") as json_fp:
                json.dump(log_data, json_fp, ensure_ascii=False, indent=4)
        except:
            return False
        
        return True
    
    
    def get_global_ip_address (self, ip_address_api):
        try:
            with urllib.request.urlopen(urllib.request.Request(ip_address_api), timeout=10) as response:
                self.global_ip_address = response.read().decode()
            
            self.add_log("・グローバルIPアドレス: " + self.global_ip_address + "\n")
        except:
            self.add_log(traceback.format_exc(), True)
            
            self.execution_succeeded = False
            
            return False
        
        return True
    
    
    def check_recv (self, sock_recv):
        recv_str = sock_recv.decode()
        
        if "COMMAND SUCCESSFUL" in recv_str:
            self.add_log(recv_str)
            
            return True
        else:
            self.add_log(recv_str, True)
            
            self.execution_succeeded = False
            
            return False
    
    
    def update_dns_records (self, dns_host, dns_port, onamae_id, password, domains):
        if self.global_ip_address == None:
            return False
        
        try:
            ctx = ssl.create_default_context()
            
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(10)
                
                with ctx.wrap_socket(sock, server_hostname=dns_host) as ssl_sock:
                    self.add_log("・" + dns_host + ":" + str(dns_port) + " に接続\n")
                    
                    ssl_sock.connect((dns_host, dns_port))
                    
                    if not self.check_recv(ssl_sock.recv(1024)):
                        return False
                    
                    self.add_log("・ID " + onamae_id + " でログイン\n")
                    
                    ssl_sock.send(b"LOGIN\r\nUSERID:" + onamae_id.encode() + b"\r\nPASSWORD:" + password.encode() + b"\r\n.\r\n")
                    
                    if not self.check_recv(ssl_sock.recv(1024)):
                        return False
                    
                    error_occurred = False
                    
                    for domain_data in domains:
                        self.add_log("・")
                        
                        if "host_name" in domain_data:
                            self.add_log(domain_data["host_name"] + ".")
                        else:
                            domain_data["host_name"] = ""
                        
                        self.add_log(domain_data["domain_name"] + " のAレコードを更新\n")
                        
                        ssl_sock.send(b"MODIP\r\nHOSTNAME:" + domain_data["host_name"].encode() + b"\r\nDOMNAME:" + domain_data["domain_name"].encode() + b"\r\nIPV4:" + self.global_ip_address.encode() + b"\r\n.\r\n")
                        
                        if not self.check_recv(ssl_sock.recv(1024)):
                            error_occurred = True
                    
                    self.add_log("・ログアウト\n")
                    
                    ssl_sock.send(b"LOGOUT\r\n.\r\n")
                    
                    if not self.check_recv(ssl_sock.recv(1024)):
                        return False
                    
                    if error_occurred:
                        return False
        except:
            self.add_log(traceback.format_exc(), True)
            
            self.execution_succeeded = False
            
            return False
        
        return True