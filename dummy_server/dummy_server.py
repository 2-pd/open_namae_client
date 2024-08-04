# coding: utf-8

import socket
import ssl


SERVER_NAME = "ddnsclient.example.jp"
SERVER_PORT = 65010
FULLCHAIN_PATH = "./fullchain.pem"
PRIVKEY_PATH = "./privkey.pem"


print("ダミーサーバを " + SERVER_NAME + ":" + str(SERVER_PORT) + " で起動します...")

ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ctx.load_cert_chain(certfile=FULLCHAIN_PATH, keyfile=PRIVKEY_PATH)

with socket.socket() as sock:
    sock.bind((SERVER_NAME, SERVER_PORT))
    
    sock.listen(1)
    
    with ctx.wrap_socket(sock, server_side=True) as ssl_sock:
        print("DDNSクライアントからのアクセスを待っています")
        
        conn, client_addr = ssl_sock.accept()
        conn.sendall(b"000 COMMAND SUCCESSFUL\r\n.\r\n")
        
        while True:
            recv_text = conn.recv(1024).decode()
            
            conn.sendall(b"000 COMMAND SUCCESSFUL\r\n.\r\n")
            
            print("\n==== 受信データ ====\n" + recv_text)
            
            if "LOGOUT" in recv_text:
                print("DDNSクライアントからログアウトメッセージが送信されました")
                break
        
        conn.shutdown(socket.SHUT_RDWR)
        conn.close()

print("\nダミーサーバの実行が完了しました")
