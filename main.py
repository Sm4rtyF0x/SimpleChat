import socket
import threading
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
DISMSG = "!disconnect"
CLIENT = []


# Burada gelen mesajları clientlara iletiyoruz.
def chat_broadcast(msg):
    for i in CLIENT:
        i.send(msg.encode(FORMAT))


# Burada gelen kullanıcın kullanıcı adını ve msajlarını alıyoruz ve chat_broadcast() fonksiyonuna gönderiyoruz.
def client_handler(conn):
    username = conn.recv(HEADER).decode(FORMAT)
    chat_broadcast(f"[{Fore.GREEN + username +Fore.RESET}] has joined.")
    while True:
        msg = conn.recv(HEADER).decode(FORMAT)
        if msg == DISMSG:
            chat_broadcast(f"[{Fore.GREEN + username + Fore.RESET}] Disconnected!")
            print("Active users", threading.active_count() - 1)
            break
        else:
            chat_broadcast(f"[{Fore.GREEN + username + Fore.RESET}] {msg}")


# Burada server'ı oluşturuyoruz ve servera bağlanan kullanıcıları kabul ediyoruz.
def server():
    SOCKET.bind((IPADDR, PORTNM))
    SOCKET.listen()
    print("["+Fore.GREEN+"LISTINING"+Fore.RESET+"] on "+Fore.GREEN + f"{IPADDR}:{PORTNM}"+Fore.RESET)
    while True:
        (conn, addr) = SOCKET.accept()
        print(f"[" + Fore.GREEN + "NEW CONNECTION" + Fore.RESET + "] " + Fore.GREEN + f"{addr}" + Fore.RESET + " connected.")
        CLIENT.append(conn)
        user = threading.Thread(target=client_handler, args=(conn,))
        user.start()
        print("Active users", threading.active_count() - 1)


server()
