import requests
import json
from config import config

app_name = 'MYPUBGSTATSBOT'

token = config.config["pubg_token"]

url = "endpoint-url"

header = {
    "Authorization": "Bearer " + token,
    "Accept": "application/vnd.api+json"
}


async def initialize_pubg_db():
    columns = ['playername', 'accountid']


async def get_player_account_id(player_name):
    try:
        link = "https://api.pubg.com/shards/steam/players?filter[playerNames]=" + str(player_name)
        r = requests.get(link, headers=header)
        json_data = r.json()
        return str(json_data["data"][0]["id"])

    except:
        return "Giocatore non trovato. Digitare un nick pubg esistente. Hai digitato : "


"""
async def get_player_stats_temp():

    seasonid = await get_current_season()
    print("seasonid="+seasonid)

    #season_list = await get_all_seasons()
    #for i in season_list:
    #    print(i)

    link = "https://api.pubg.com/shards/steam/players?filter[playerNames]=BIAMephisto,Corny6,cucHor,Maycool,Cesco10,Avdax"
    r = requests.get(link, headers=header)

    json_data = r.json()
    allstats = []
    for entry in json_data["common"]:
        playerstats = entry["attributes"]["name"]
        playerid = entry["id"]
        print(playerstats + ":" + playerid)
        allstats.append(playerstats + ":" + playerid)


        #seasonid = await get_current_season()
        #print("seasonid="+seasonid)
        #for player in i["attributes"]:
        #    print(str(player.get("name")))
    #print(json_data["common"])
    return allstats
"""


async def get_all_seasons():
    link = "https://api.pubg.com/shards/steam/seasons/"
    r = requests.get(link, headers=header)
    season_list = []
    json_data = r.json()
    for entry in json_data["data"]:
        season_list.append(entry["id"])

    return season_list


async def get_current_season():
    link = "https://api.pubg.com/shards/steam/seasons/"
    r = requests.get(link, headers=header)
    seasonlist = []
    json_data = r.json()
    print(json_data)
    for entry in json_data["data"]:
        if entry["attributes"]["isCurrentSeason"]:
            return entry["id"]


"""
async def get_player_details_det(account_id, season_id):

    non usata
    :param account_id:
    :param season_id:
    :return:
    link = "https://api.pubg.com/shards/steam/players/" + account_id + "/seasons/" + season_id
    r = requests.get(link, headers=header)

    json_data = r.json()
    rank_points =  json_data["common"]["attributes"]["gameModeStats"]["squad-fpp"]["rankPoints"]
    #match_played = json_data["common"]["attributes"]["gameModeStats"]["squad-fpp"]["bestRankPoint"]
    wins = json_data["common"]["attributes"]["gameModeStats"]["squad-fpp"]["wins"]
    kills = json_data["common"]["attributes"]["gameModeStats"]["squad-fpp"]["kills"]
    headshots = json_data["common"]["attributes"]["gameModeStats"]["squad-fpp"]["headshotKills"]
    top_ten = json_data["common"]["attributes"]["gameModeStats"]["squad-fpp"]["top10s"]
    longest_kill = json_data["common"]["attributes"]["gameModeStats"]["squad-fpp"]["longestKill"]

    text = "Points:" + str(rank_points) + " Wins:" + str(wins) + " Kills:" + str(kills) + " LongestKill:" + str(longest_kill) + " HeadShot kills:" + str(headshots)
    print(text)
    return text
"""


async def get_player_details(account_id, season_id):
    link = "https://api.pubg.com/shards/steam/players/" + account_id + "/seasons/" + season_id
    r = requests.get(link, headers=header)
    json_data = r.json()
    print(json_data)

    return json_data["data"]["attributes"]["gameModeStats"]["squad-fpp"]


async def get_players_stats(player_ids):
    # print(player_ids)
    link = "https://api.pubg.com/shards/steam/players?filter[playerIds]=" + str(player_ids)
    r = requests.get(link, headers=header)

    json_data = r.json()
    print(json_data)
    return json_data


async def get_player_lifetime(account_id):
    link = "https://api.pubg.com/shards/steam/players/" + account_id + "/seasons/lifetime"
    r = requests.get(link, headers=header)

    json_data = r.json()
    # print(json_data[""])
    # print(r)
    return json_data["data"]["attributes"]["gameModeStats"]["squad-fpp"]
