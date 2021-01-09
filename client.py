import socket
import threading
import time
from colorama import Fore
import platform
import os

if platform.system() == "Windows":
    os.system("cls")
elif platform.system() == "Linux":
    os.system("clear")

HEADER = 1024
IPADDR = "192.168.1.36"
PORTNM = 9999
FORMAT = "UTF-8"
SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
USERNAME = input("Enter your username: ").encode(FORMAT)
DISMSG = "!disconnect"
CLIENT = []


# Burada servera gelen diğer mesajları görüntülüyoruz
def listener():
    while True:
        msg = SOCKET.recv(HEADER).decode(FORMAT)
        if USERNAME.decode(FORMAT) in msg:
            parse = msg.split("] ")
            if parse[1] == DISMSG:
                break
            else:
                continue
        else:
            print(msg)


# Burada kullanıcı adını ve mesajları server'a iletiyoruz.
def client():
    SOCKET.connect((IPADDR, PORTNM))
    SOCKET.send(USERNAME)
    while True:
        input()
        time.sleep(.1)
        msg = input(f"[{Fore.YELLOW + USERNAME.decode(FORMAT) + Fore.RESET}] ").encode(FORMAT)
        print(Fore.RESET)
        if msg == DISMSG:
            SOCKET.send(msg)
            break
        else:
            SOCKET.send(msg)


# Burada 2 fatklı thread oluşturuyoruz.
client_t = threading.Thread(target=client)
listener_t = threading.Thread(target=listener)
client_t.start()
listener_t.start()
