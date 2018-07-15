import socket
import time

HOST = "irc.server"
PORT = 6667  # default 6667
NICK = "bot_nick"
MASTER = "master_nick"
MASTER_HOST = "master@host.xx"
CHANNEL = "#channel"
TIMEOUT = 30  # in seconds


def server_connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))

    s.sendall(bytes(f"NICK {NICK}\r\n", "utf-8"))
    s.sendall(bytes("USER %s %s %s :%s\r\n" % (NICK, NICK, NICK, NICK), "utf-8"))
    s.sendall(bytes(f"JOIN {CHANNEL}\r\n", "utf-8"))

    while 1:
        ircmsg = s.recv(1024).decode("utf-8")
        print(ircmsg)

        line = [x for x in ircmsg.splitlines() if "353" in x]

        if line:
            single = line[0]
            nick_list = single.split()[5:]
            if len(nick_list) == 1 and f":@{NICK}" not in nick_list:
                print("bingo")
                print(single)
                s.sendall(bytes(f"PART {CHANNEL}\r\n", "utf-8"))
                s.sendall(bytes(f"JOIN {CHANNEL}\r\n", "utf-8"))

            if len(nick_list) == 1 and f":@{NICK}" in nick_list:
                print("ADMIN")
                s.sendall(bytes(f"PRIVMSG {MASTER} :ADMIN {CHANNEL} \r\n", "utf-8"))

            if len(nick_list) != 1 and f":@{NICK}" not in nick_list:
                print("fail")
                print(single)
                time.sleep(TIMEOUT)
                s.sendall(bytes(f"NAMES {CHANNEL}\r\n", "utf-8"))

        if "PING" in ircmsg:
            s.sendall(bytes(f"PONG :{HOST}\r\n", "utf-8"))

        if f":{MASTER}!{MASTER_HOST} JOIN :{CHANNEL}" in ircmsg:
            s.sendall(bytes(f"MODE {CHANNEL} +o {MASTER}\r\n", "utf-8"))


server_connect()

