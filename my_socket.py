# -*-coding:UTF-8 -*
import chardet
import socket
import sys


# decode ce qui a été reçu avec le bon encodage
def recv_and_decode(readbuffer):
    preferred_encs = ["UTF-8", "cp_utf8", "CP1252", "ISO-8859-1", "iso8859_2", "cp858", "cp65001", "iso8859_15",
                      "cp500", "mac_roman", "ascii"]
    changed = False
    for enc in preferred_encs:
        try:
            res = readbuffer.decode(enc)
        except:
            continue
        changed = True
        break
    if not changed:
        try:
            enc = chardet.detect(readbuffer)['encoding']
            res = readbuffer.decode(enc)
        except:
            res = readbuffer.decode(enc, 'ignore')
    return res


class Socket():
    def __init__(self):
        self.HOST = "irc.rizon.net"
        self.PORT = 6667
        
        self.NICK = "XXXX"
        self.IDENT = "XXXX"
        self.REALNAME = "XXXX"
        self.MASTER = "XXXX"
        self.PWD = "XXXX"
        

        self.connected = False
        self.s = socket.socket()

    def connect(self):
        try:
            self.s.connect((self.HOST, self.PORT))
            self.connected = True
        except:
            print("*** connection �chou�e ***")
            exit()
        print("---- connection done ----")

    def send_data(self):
        """ envoie les infos
        """
        self.s.send(bytes("NICK %s\r\n" % self.NICK, "UTF-8"))
        self.s.send(bytes("USER %s %s bla :%s\r\n" % (self.IDENT, self.HOST, self.REALNAME), "UTF-8"))
        self.s.send(bytes("NS IDENTIFY %s\r\n" % self.PWD, "UTF-8"))
        self.s.send(bytes("HS ON\r\n", "UTF-8"))
        print("---- data send ----")

        self.s.send(bytes("NOTICE %s :Hello Master\r\n" % self.MASTER, "UTF-8"))
        self.join("#labonnebraise")

    def recv_decode(self, readlines):
        readbuffer = self.s.recv(1024)
        return readlines + recv_and_decode(readbuffer)

    def send(self, cmd, canal, message):
        self.s.send(bytes(cmd + " " + canal + " " + message + "\r\n", "UTF-8"))

    def ping(self, line):
        """ answer to ping
        :param line:
        """
        self.s.send(bytes("PONG %s\r\n" % line[1], "UTF-8"))
        print(str(line))

    def join(self, canal):
        self.s.send(bytes("JOIN %s\r\n" % canal, "UTF-8"))

    def quit(self, message):
        self.s.send(bytes("QUIT %s \r\n" % message, "UTF-8"))
        self.connected = False

    def names(self, canal):
        self.s.send(bytes("NAMES %s\r\n" % canal, "UTF-8"))

    def nick(self, nick):
        self.s.send(bytes("NICK %s\r\n" % nick, "UTF-8"))

    def close(self):
        try:
            self.s.close()
        except:
            pass
