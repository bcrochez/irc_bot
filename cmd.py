# -*-coding:UTF-8 -*

from module import *

print("---- ALL MODULE LOADED ----")


#

def part(s, pseudo, canal, message):
    if pseudo == s.MASTER:
        if len(message) > 1:
            s.send("PART", message[1], ":Adios amigos!")
        else:
            s.send("PART", canal, ":Adios amigos!")


def send_help(s, pseudo, canal, message):
    s.send("NOTICE", pseudo, ":!modo pour avoir la liste des modérateurs présents sur le canal.")
    # if 'Transformice' in canal:
    aide_transformice(s, pseudo, canal, message)
    s.send("NOTICE", pseudo, ":!aide pour afficher cette aide.")
    s.send("NOTICE", pseudo, ":!extracmd pour avoir plus de commandes.")


def aide_transformice(s, pseudo, canal, message):
    # s.send("NOTICE",pseudo,":Si tu as un souci en jeu essaye de contacter un modérateur!")
    # s.send("NOTICE",pseudo,":Sinon tu peux contacter les administrateurs via le formulaire sur www.transformice.com/contact")
    s.send("NOTICE", pseudo,
           ":\x02!omodo\x02 pour avoir la liste des \x02modérateurs\x02 et \x02administrateurs\x02 connectés en jeu.")
    s.send("NOTICE", pseudo, ":\x02!mapcrewte\x02 pour avoir les membres du \x02mapcrew\x02 en ligne.")
    s.send("NOTICE", pseudo, ":\x02!senti\x02 pour avoir les \x02sentinelles fr\x02 en ligne.")
    s.send("NOTICE", pseudo, ":!stats <nom de la souris> pour avoir les statistiques d'une souris.")
    s.send("NOTICE", pseudo, ":!tribu <nom de la tribu> pour avoir les infos d'une tribu.")


def extra_cmd(s, pseudo, canal, message):
    s.send("NOTICE", pseudo, ":!info pour avoir des infos utiles.")
    s.send("NOTICE", pseudo, ":!tank <nom d'un char> pour avoir les infos d'un char.")
    s.send("NOTICE", pseudo, ":!tanklist <nation> pour avoir la liste des chars d'une nation.")
    s.send("NOTICE", pseudo,
           ":!statwot <pseudo d'un joueur> pour avoir les statistiques du joueur (sur World of Tanks).")
    s.send("NOTICE", pseudo, ":!steamgame <nom du jeu> pour avoir des infos sur un jeu de steam.")
    # s.send("NOTICE",pseudo,":!meteo <lieu> pour avoir la météo d'un lieu.")
    if len(citations.names) == 0:
        s.send("NOTICE", pseudo,
               ":!citation <theme>(optionnel) pour obtenir une citation au hasard. Thèmes disponibles: aucun thème n'est disponible.")
    else:
        s.send("NOTICE", pseudo,
               ":!citation <theme>(optionnel) pour obtenir une citation au hasard. Thèmes disponibles: " + " ".join(
                   citations.names))


def stat_wot(s, pseudo, canal, message):
    to_send = ":Joueur inconnu!"
    if len(message) > 1:
        try:
            nickname, nb_battles, nb_wins, nb_frags, max_frags, max_dmg = wot.get_common_data(message[1])
            if nickname == message[1]:
                to_send = ":" + nickname + " a participé à " + str(nb_battles) + " battailles! V: " + str(
                    nb_wins) + " - frags: " + str(nb_frags) + " - max frag: " + str(max_frags) + " - max dmg: " + str(
                    max_dmg)
        except:
            to_send = ":Joueur inconnu!"
        if canal[0] == '#':
            s.send("NOTICE", pseudo, to_send)
        else:
            s.send("PRIVMSG", pseudo, to_send)


def send_tank(s, pseudo, canal, message):
    tank_name = " ".join(message[1:])
    try:
        real_name, nation, type_, description = wot.get_info_tank(tank_name)
        to_send = ":" + real_name + " (" + type_ + ") - " + nation + " - " + description
    except:
        to_send = ":Char inconnu!"
    s.send("NOTICE", pseudo, to_send)


def send_tank_list(s, pseudo, canal, message):
    tank_list = wot.get_tank_list()
    tank_list_s = wot.get_tank_list_s()
    if len(message) == 1:
        nations = []
        for nation in tank_list_s:
            nations.append(nation)
        s.send("NOTICE", pseudo,
               ":Il y a " + str(len(tank_list)) + " tanks dans la base de données. Nations disponibles: " + " ".join(
                   nations))
    elif message[1].lower() == "all":
        for nation in tank_list_s:
            to_send = ":" + nation
            tank_to_send = []
            for type_ in tank_list_s[nation]:
                for tank_id in tank_list_s[nation][type_]:
                    tank = tank_list[tank_id]
                    tank_to_send.append(tank["short_name_i18n"])
            to_send += " (" + str(len(tank_to_send)) + " tanks): " + ', '.join(tank_to_send)
            s.send("NOTICE", pseudo, to_send)
    else:
        try:
            tank_nation = tank_list_s[message[1]]
        except:
            s.send("NOTICE", pseudo, ":Nation inconnue!")
            return
        for type_ in tank_nation:
            to_send = ":" + type_
            tank_to_send = []
            for tank_id in tank_nation[type_]:
                tank = tank_list[tank_id]
                tank_to_send.append(tank["short_name_i18n"])
            to_send += " (" + str(len(tank_to_send)) + " tanks): " + ', '.join(tank_to_send)
            s.send("NOTICE", pseudo, to_send)


def load_quote(s, pseudo, canal, message):
    if pseudo != s.MASTER:
        return
    if len(message) > 1:
        if citations.load_cita_theme(message[1]) == 1:
            s.send("NOTICE", s.MASTER, ":Citations " + message[1] + " chargées avec succès.")
        else:
            s.send("NOTICE", s.MASTER, ":Echec du chargement de " + message[1] + ".")
    else:
        try:
            citations.load_citations()
            s.send("NOTICE", s.MASTER, ":Citations chargées avec succès.")
        except:
            s.send("NOTICE", s.MASTER, ":Echec du chargement des citations.")


def send_citation(s, pseudo, canal, message):
    if canal[0] == '#':
        cmd = "NOTICE"
    else:
        cmd = "PRIVMSG"
    if len(message) > 1:
        try:
            citation = citations.get_citation_by_theme(message[1])
            for bout in citation.split('\n'):
                to_send = ':' + bout
                s.send(cmd, pseudo, to_send)
        except:
            to_send = ":Thème inconnu!"
            s.send(cmd, pseudo, to_send)
    else:
        try:
            citation = citations.get_random_citation()
            for bout in citation.split('\n'):
                to_send = ':' + bout
                s.send(cmd, pseudo, to_send)
        except:
            to_send = ":Aucune citation trouvée dans la base!"
            s.send(cmd, pseudo, to_send)


def send_pizza(s, pseudo, canal, message):
    if canal[0] == '#':
        s.send("PRIVMSG", canal,
               ":ACTION envoie une pizza " + " ".join(message[1:]) + " à la figure de " + pseudo + ", fais la toi même !")
    else:
        s.send("PRIVMSG", pseudo,
               ":ACTION envoie une pizza " + " ".join(message[1:]) + " à la figure de " + pseudo + ", fais la toi même !")


def send_cafe(s, pseudo, canal, message):
    s.send("NOTICE", pseudo, ":Je suis pas une cafetière!")


def send_steamgame(s, pseudo, canal, message):
    if len(message) > 1:
        name, release, price, avis = steam.get_data(' '.join(message[1:]))
        s.send("NOTICE", pseudo, ":" + name + " - sorti le " + release + " - prix: " + price + " - avis: " + avis)


def send_weather(s, pseudo, canal, message):
    try:
        if len(message) > 1:
            real_name, description, temp, humidity, pression, country = meteo.get_weather(" ".join(message[1:]))
        else:
            real_name, description, temp, humidity, pression, country = meteo.get_weather()
        to_send = ":" + real_name + "(" + country + "), temps " + description.lower() + " - " + str(
            temp) + "°C - " + str(humidity) + "% d'humidité - pression atmosphérique de " + str(pression) + "hpa"
    except:
        to_send = ":Il doit y faire beau"
    if canal[0] == '#':
        cmd = "NOTICE"
    else:
        cmd = "PRIVMSG"
    s.send(cmd, pseudo, to_send)


def send_mapcrew(s, pseudo, canal, message):
    mapcrews = transfo.get_mapcrew()
    if len(mapcrews) == 0:
        to_send = ":Aucun mapcrew trouvé!"
    else:
        to_send = ":"
        to_send += " - ".join([typem + ": " + mapcrews[typem] for typem in mapcrews])
    # s.send("NOTICE", pseudo, to_send)
    s.send("NOTICE", pseudo, ":Cfm bot cassé")


def send_senti(s, pseudo, canal, message):
    # senti = ":" + transfo.get_sentinelle()["fr"]
    # s.send("NOTICE", pseudo, senti)
    s.send("NOTICE", pseudo, ":Cfm bot cassé")


def send_omodo(s, pseudo, canal, message):
    atleast_a_modo = False
    mods, admin = transfo.get_online_mods()
    to_send = ':'
    mod_by_id = []
    for id_p in mods:
        if len(mods[id_p]) != 0:
            atleast_a_modo = True
            mods_tmp = []
            for mod in mods[id_p]:
                if mod in admin:
                    mods_tmp.append('\x034' + mod + '\x03')
                else:
                    mods_tmp.append(mod)
            mod_by_id.append("\x032\x02" + id_p + "\x02\x03" + ": " + (', '.join([mod for mod in mods_tmp])))
    if not atleast_a_modo:
        # s.send("NOTICE", pseudo, to_send+"Personne ne modère!")
        pass
    else:
        to_send += ' - '.join(mod_by_id)
        # s.send("NOTICE", pseudo, to_send)
    s.send("NOTICE", pseudo, ":Cfm bot cassé")


def send_modo(s, pseudo, canal, message, listOfMod):
    low_canal = canal.lower()
    size = len(listOfMod[low_canal])
    if size == 0:
        to_send = ":Aucun modérateur n'est connecté!"
    else:
        to_send = ":Les modérateurs connectés sur ce canal sont:"
    i = 0
    while i < size:
        if size != 1 and i == size - 1:
            to_send += " et"
        to_send += " " + listOfMod[low_canal][i]
        i += 1
    s.send("NOTICE", pseudo, to_send)


def send_yt(s, canal, message):
    title, views, date = youtube.get_title_and_views(message)
    if 'Transformice' in canal:
        if (sum(1 for c in title if c.isupper()) >= 9):
            to_send = ":Youtube: " + title.lower() + " (" + date.lower() + " - " + views + " vues)"
        else:
            to_send = ":Youtube: " + title + " (" + date.lower() + " - " + views + " vues)"
    else:
        to_send = ":\x02Youtube\x02: " + title + " (" + date.lower() + " - " + views + " vues)"
    s.send("PRIVMSG", canal, to_send)


def send_topic_title(s, canal, message):
    title = transfo.get_topic_title(message)
    if 'Transformice' in canal:
        if (sum(1 for c in title if c.isupper()) >= 6):
            to_send = ":Forum TFM: " + title.lower()
        else:
            to_send = ":Forum TFM: " + title
    else:
        to_send = ":\x02Forum TFM\x02: " + title
    s.send("PRIVMSG", canal, to_send)


def send_time(s, pseudo, canal, message):
    if len(message) > 1:
        name, h, m, sd, tz = google.get_time_by_geoloc(' '.join(message[1:]))
    else:
        name, h, m, sd, tz = google.get_time_by_geoloc()
    s.send("NOTICE", pseudo, ":" + name + ": " + str(h) + "h" + str(m) + "m" + str(sd) + "s (" + tz + ")")


cmds = {}
cmds['!help'] = cmds['!aide'] = send_help
cmds['!extracmd'] = extra_cmd
cmds['!omodo'] = send_omodo
cmds['!mapcrewte'] = send_mapcrew
cmds['!senti'] = send_senti
cmds['!statwot'] = stat_wot
cmds['!tank'] = send_tank
cmds['!tanklist'] = send_tank_list
cmds['!meteo'] = send_weather
cmds['!citation'] = send_citation
cmds['!steamgame'] = send_steamgame
cmds['!pizza'] = send_pizza
cmds['!café'] = cmds['!cafe'] = send_cafe
cmds['!part'] = part
cmds['!loadq'] = load_quote
cmds['!time'] = send_time
# cmds['!tape'] = lambda s,p,c,m:s.send("PRIVMSG", c,":ACTION tape " + p + "")
