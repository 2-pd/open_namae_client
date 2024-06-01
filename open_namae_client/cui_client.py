# coding: utf-8

import sys
import os
import time
import random
import json

import open_namae


if "-s" in sys.argv:
    silent_mode = True
else:
    silent_mode = False

if "-i" not in sys.argv:
    if not silent_mode:
        print("処理の開始を遅延しています...")
    
    time.sleep(random.randint(11,50))

ddns_client = open_namae.ddns_client(silent_mode)

try:
    with open(os.path.dirname(os.path.abspath(__file__)) + "/config.json", "r", encoding="utf-8") as json_fp:
        config = json.load(json_fp)
except:
    ddns_client.add_log("接続設定情報が読み込めませんでした", True)
    ddns_client.save_log()
    
    sys.exit()

if "-f" in sys.argv or ddns_client.get_global_ip_address(config["ip_address_api"]):
    if ddns_client.check_update_needed(config["modified_datetime"]):
        ddns_client.update_dns_records(config["dns_host"], config["dns_port"], config["onamae_id"], config["password"], config["domains"])
        
        ddns_client.save_log()
        
        if not silent_mode and ddns_client.execution_succeeded:
            print("DNS情報を更新しました")
    else:
        if not silent_mode:
            print("DNS情報は更新不要です")
