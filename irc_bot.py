# -*-coding:UTF-8 -*

import my_socket
import cmd
import threading

VERSION = "3.5"


def parse_prvmsg(s, listOfMod, pseudo, canal, message):
    first_word = message[0]
    if pseudo in ignore_list:
        return
    if first_word == '\x01PING':
        s.send("NOTICE", pseudo, "PONG!")
    elif first_word == '\x01VERSION\x01':
        s.send("NOTICE", pseudo, ":" + s.NICK + " version " + VERSION + " par " + s.MASTER)
    if first_word.startswith('!'):
        try:
            cmds[first_word.lower()](s, pseudo, canal, message)
        except KeyError:
            print("error while processing command : "+first_word)
    if canal[0] == '#':
        for msg in message:
            if msg.startswith("http://www.youtube.com/watch") or msg.startswith("https://www.youtube.com/watch"):
                cmd.send_yt(s, canal, msg)
            if msg.startswith("http://atelier801.com/topic?"):
                cmd.send_topic_title(s, canal, msg)


# quand le bot reçoit un notice
def parse_notice(s, listOfChan, pseudo, message):
    if pseudo.lower() == s.MASTER.lower():
        if message[0] == "join":
            s.join(message[1])
        elif message[0] == "part":
            s.send("PRIVMSG", message[1], ":Je m'en vais comme un prince!")
            s.send("PART", message[1], ":Je m'en vais comme un prince!")
        elif message[0] == "exit":
            to_send = ":Je m'en vais comme un prince!"
            for chan in listOfChan:
                s.send("PRIVMSG", chan, to_send)
            s.quit(to_send)
        elif message[0] == "send_data":
            s.send_data()
        elif message[0] == "stop" or message[0] == "shutdown":
            s.quit(":Shuting down")
        elif message[0] == "nick":
            s.nick(message[1])
        else:
            chan = message[0]
            s.send("PRIVMSG", chan, ":" + " ".join(message[1:]))


# récupère la liste des opérateurs
def get_mods(listOfMod, message):
    size = len(message)
    i = 0
    while i < size:
        newMod = ""
        toAdd = 0
        for char in message[i]:
            if (char == "@"):
                toAdd = 1
            elif (char != ":" and toAdd == 1):
                newMod += char
        if (toAdd == 1 and newMod not in listOfMod[message[1].lower()]):
            listOfMod[message[1].lower()].append(newMod)
        toAdd = 0
        i += 1
    print(listOfChan, listOfMod)


# quand quelqu'un rejoint un canal
def join_canal(s, listOfChan, listOfMod, pseudo, canal):
    if pseudo == s.NICK:
        low_canal = canal.lower()
        if low_canal not in listOfChan:
            listOfChan.append(low_canal)
            listOfMod.setdefault(low_canal, [])
            # s.names(canal)
            # s.send("NOTICE", pseudo, ":Salut " + pseudo + "! Bienvenue sur le canal \x02" + canal + "\x02. Tape \x02!aide\x02 si tu as besoin d'aide.")


# quand quelqu'un part ou est kické le canal
def part_or_kick(listOfMod, pseudo, canal):
    if pseudo in listOfMod[canal.lower()]:
        listOfMod[canal.lower()].remove(pseudo)


# quand quelqu'un quitte le canal
def so_quit(listOfChan, listOfMod, pseudo):
    for chan in listOfChan:
        if pseudo in listOfMod[chan]:
            listOfMod[chan].remove(pseudo)


# obtient le pseudo depuis la ligne reçue
def get_pseudo(nick):
    nick = str(nick).strip(":")
    return nick.split("!")[0]


# quand quelqu'un change de mode
def mode(s, listOfMod, canal, message):
    if message[0].startswith('+') and "o" in message[0]:
        listOfMod[canal.lower()].append(message[1])
    elif message[0].startswith('-') and "o" in message[0]:
        if message[1] in listOfMod[canal.lower()]:
            listOfMod[canal.lower()].remove(message[1])
            # elif message[0] == "+b":
            # s.send("PRIVMSG", canal, ":HEADSHOT")


# découpe une ligne reçue
def parse_line(line):
    pseudo = get_pseudo(line[0])
    cmd = line[1]
    size = len(line)
    if cmd == "QUIT":
        if size == 2:
            return cmd, pseudo, [], []
        else:
            if size == 3:
                return cmd, pseudo, [], [str(line[2])[1:]]
            else:
                return cmd, pseudo, [], [str(line[2])[1:]] + line[3:]
    canal = str(line[2]).lstrip(':')
    if size == 3:
        return cmd, pseudo, canal, []
    elif size == 4:
        return cmd, pseudo, canal, [str(line[3])[1:]]
    else:
        return cmd, pseudo, canal, [str(line[3])[1:]] + line[4:]


def parse(s, line, listOfChan, listOfMod):
    line = str.rstrip(line)
    line = str.split(line)
    if line[0] == "PING":
        s.ping(line)
        return
    cmd, pseudo, canal, message = parse_line(line)
    try:
        print(cmd, pseudo, canal, message)
    except:
        print("erreur d'affichage")

    if cmd == "JOIN":
        join_canal(s, listOfChan, listOfMod, pseudo, canal)
    if cmd == "MODE":
        mode(s, listOfMod, canal, message)
    if cmd == "QUIT":
        so_quit(listOfChan, listOfMod, pseudo)
    if cmd == "PART" or cmd == "KICK":
        part_or_kick(listOfMod, pseudo, canal)
    if cmd == "353":
        get_mods(listOfMod, message)
    if cmd == "PRIVMSG":
        parse_prvmsg(s, listOfMod, pseudo, canal, message)
    if cmd == "NOTICE" and canal == s.NICK:
        parse_notice(s, listOfChan, pseudo, message)


def listen(s, listOfChan):
    while True:
        try:
            notice = input('>')
            parse_notice(s, listOfChan, s.MASTER, notice.split(" "))
        except:
            return


def quitte(s, pseudo, canal, message):
    if pseudo == s.MASTER:
        s.quit(":Ne me tue pas :(")
    else:
        s.send("NOTICE", pseudo, ":Tu n'es pas mon maître, infâme traitre!")


# s.send(bytes("JOIN #transformicefr2\r\n", "UTF-8"))
# s.send(bytes("JOIN #pouletbot\r\n", "UTF-8"))


listOfChan = []
listOfMod = {}
ignore_list = []
cmds = {}
cmds.update(cmd.cmds)
cmds['!modo'] = lambda s, p, c, m: cmd.send_modo(s, p, c, m, listOfMod)
cmds['!info'] = lambda s, p, c, m: s.send("NOTICE", p, ":Je suis PouletBot, le robot génie de Pouletbraise!")
cmds['!secret'] = lambda s, p, c, m: s.send("NOTICE", p, ":Circulez, y'a rien à voir")
cmds['!kill'] = quitte


def serve(s, listOfChan, listOfMod):
    readlines = ""
    scan = threading.Thread(target=listen, args=(s, listOfChan))
    scan.setDaemon(True)
    scan.start()

    while s.connected:
        try:
            readlines = s.recv_decode(readlines)
        except ConnectionAbortedError:
            print("Connexion perdue")
            exit()
        except OSError:
            print("Erreur système")
            exit()

        temp = str.split(readlines, "\n")
        readlines = temp.pop()

        for line in temp:
            t = threading.Thread(target=parse, args=(s, line, listOfChan, listOfMod))
            t.start()
            # t.run()


if __name__ == '__main__':
    try:
        s = my_socket.Socket()
        s.connect()
        s.send_data()

        serve(s, listOfChan, listOfMod)

        s.close()
    except:
        import sys

        print(sys.exc_info()[0])
        print("---- -----")
        import traceback

        print(traceback.format_exc())
        print("---- -----")
        print("Press Enter to continue ...")
        input()
