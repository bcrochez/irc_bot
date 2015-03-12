import json
import urllib.request

print("---- start loading tanks data ----")
application_id = "XXXX"

try:
    tanks_b = urllib.request.urlopen("http://api.worldoftanks.eu/wot/encyclopedia/tanks/?application_id="+application_id+"&language=fr").read()
    tanks = json.loads(tanks_b.decode())["data"]
except:
    print("*** connection to wot api failed ***")
print("---- tanks data loaded ----")

def get_common_data(player_name):
    data_b = urllib.request.urlopen("https://api.worldoftanks.eu/wot/account/list/?application_id="+application_id+"&search="+player_name).read()
    data = json.loads(data_b.decode())

    player_id = str(data["data"][0]["account_id"])

    player_data_b = urllib.request.urlopen("https://api.worldoftanks.eu/wot/account/info/?application_id="+application_id+"&account_id="+player_id).read()
    player_data = json.loads(player_data_b.decode())["data"][player_id]
    
    nickname = player_data["nickname"]
    nb_battles = player_data["statistics"]["all"]["battles"]
    nb_wins = player_data["statistics"]["all"]["wins"]
    nb_frags = player_data["statistics"]["all"]["frags"]
    max_frags = player_data["statistics"]["max_frags"]
    max_dmg = player_data["statistics"]["max_damage"]
    return nickname, nb_battles, nb_wins, nb_frags, max_frags, max_dmg

def get_info_tank(tank_name):
    for tank_id in tanks:
        if tanks[tank_id]["short_name_i18n"].lower() == tank_name.lower():
            tank_details = tanks[tank_id]
            #tank_id = str(tank_data["tank_id"])
            #tank_details_b = urllib.request.urlopen("http://api.worldoftanks.eu/wot/encyclopedia/tankinfo/?application_id="+application_id+"&tank_id="+tank_id).read()
            #tank_details = json.loads(tank_details_b.decode())["data"][tank_id]
            #print(tank_details)
            name = tank_details["name_i18n"]
            nation = tank_details["nation_i18n"]
            type_ = tank_details["type_i18n"].lower()
            #weight = str(tank_details["weight"])
            return name, nation, type_