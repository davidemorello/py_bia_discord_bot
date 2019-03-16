from config import config
from pubg import pubg_stats_api
import json
import asyncio
from pubg import pubg_rank_generator
from datetime import datetime
import random

pubg_file = config.config['pubg_file']
pubg_player_stats = config.config['pubg_player_stats']
min_played_match = int(config.config["min_played_match"])


async def build_teams(members, gametype):
    """

    :param members:
    :param gametype:
    :return:
    """
    playerlist = []
    result = []
    for m in members:
        ran = random.choice(range(1, 1000))
        playerlist.append([m, ran])


    playerlist.sort(key=lambda x: (x[1]), reverse=True)
    if(gametype == "duo"):
        return
    elif(gametype == "squad"):
        return


# region Chiamate API pubg LIVE
async def unregister_pubg_player(player_name):
    """
    rimuove membro da file users e stats
    :param player_name:
    :return:
    """
    # rimuovo da file users
    with open(pubg_file) as file:

        data = json.load(file)
        i = 0
        for row in data['users']:
            if player_name == row["player_name"]:
                print("Rimozione membro : " + row["player_name"])
                print(data['users'][i])
                del data['users'][i]
            i = i + 1

    with open(pubg_file, 'w') as file:
        json.dump(data, file)

    # rimuovo da file stats
    with open(pubg_player_stats) as file:

        player_stats = json.load(file)
        for player in player_stats:
            print(player)
            if player_name == player:
                print("Rimozione membro : " + player)
                del player_stats[player]
                break

    with open(pubg_player_stats, 'w') as file:
        json.dump(player_stats, file)

    return "Membro rimosso: " + player


async def register_pubg_player(player_name):
    """
    Salva nuovo giocatore nel relativo file json (/, al fine di salvare l accountid per api pubg
    e dover fare questa chiamata alle api solo occasionalmente
    Prende anche le statistiche live e le aggiunge a file stats.json
    """
    with open(pubg_file) as file:

        data = json.load(file)

        for row in data['users']:
            if player_name == row["player_name"]:
                return 'Utente già registrato : '

    account_id = await pubg_stats_api.get_player_account_id(player_name)
    if str(account_id).startswith('account'):
        data["users"].append({'account_id': account_id, 'player_name': player_name})
    else:
        return account_id

    with open(pubg_file, 'w') as file:
        json.dump(data, file)

    await get_live_player_detail(player_name)

    return 'Giocatore registrato : '


async def sync_top10_stats():
    """
    Sincronizza i migliori 10 giocatori per score
    :return:
    """
    users_data = await get_users_data()
    season_id = users_data["season_id"]

    players_stats = await get_all_players_stats()
    players_stats_ordered = []
    result = []

    for player in players_stats:
        score = str(round(players_stats[player].get("rankPoints")))
        players_stats_ordered.append([player, score])

    players_stats_ordered.sort(key=takeSecond, reverse=True)

    i = 0
    for player in players_stats_ordered:
        if i < 10:
            account_id = await get_account_id(player[0])
            players_stats[player[0]] = await pubg_stats_api.get_player_details(account_id, season_id)
            result.append([player[0], players_stats[player[0]]])
        i = i + 1

    return result


async def sync_pubg_players_stats():
    """
    Risincronizza tutti i membri, in sleep 60 sec ogni 10 membri ciclati per via del limite api pubg
    :return:
    """

    data = await get_users_data()
    season_id = data["season_id"]

    i = 0
    users_dict = {}
    for user in data["users"]:
        if i in range(10, 100, 10):
            print("attesa 60 secondi... i = " + str(i))
            await asyncio.sleep(60)
        print("get_player_details LIVE : " + user["player_name"] + " i = " + str(i))
        users_dict[user["player_name"]] = await pubg_stats_api.get_player_details(user["account_id"], season_id)
        i = i + 1

    data["last_update"] = str(datetime.now()).split('.')[0]
    with open(pubg_file, 'w') as file:
        json.dump(data, file)

    with open(pubg_player_stats, 'w') as file:
        json.dump(users_dict, file)


async def get_live_player_detail(player_name):
    """

    :param player_name:
    :return:
    """
    users_data = await get_users_data()
    player_data = {}
    season_id = users_data["season_id"]

    with open(pubg_player_stats) as file:
        player_data = json.load(file)

    for user in users_data["users"]:
        if player_name == user["player_name"]:
            player_data[user["player_name"]] = await pubg_stats_api.get_player_details(user["account_id"], season_id)
            # player_data = await pubg_stats_api.get_player_details(user["account_id"], season_id)
            # player_data[user["player_name"]] = player_data

    with open(pubg_player_stats, 'w') as file:
        json.dump(player_data, file)

    return player_data


# endregion


# region Creazione TABELLE CLASSIFICHE
async def generate_main_players_table():
    players_stats = await get_all_players_stats()
    players_table = await pubg_rank_generator.generate_all_tables(players_stats)
    return players_table[1]


async def generate_all_classifiche():
    players_stats = await get_all_players_stats()
    classifiche = await pubg_rank_generator.generate_all_tables(players_stats)
    return classifiche[0]


async def get_lifetime_player_stats(player_name):
    """

    :param player_name:
    :return:
    """
    users_data = await get_users_data()
    player_data = {}
    season_id = users_data["season_id"]

    with open(pubg_player_stats) as file:
        player_data = json.load(file)

    account_id = await get_account_id(player_name)

    for user in users_data["users"]:
        if player_name == user["player_name"]:
            player_data[user["player_name"]] = await pubg_stats_api.get_player_lifetime(account_id)
            # player_data = await pubg_stats_api.get_player_details(user["account_id"], season_id)
            # player_data[user["player_name"]] = player_data

    return player_data

# endregion


# region GET common LOCAL
async def get_players_list():
    """

    :return:
    """
    with open(pubg_file) as file:
        data = json.load(file)

    return data["users"]


async def get_all_players_stats():
    """

    :return:
    """
    with open(pubg_player_stats) as file:
        data = json.load(file)

    return data


async def get_users_data():
    """
    get users common
    :return:
    """
    with open(pubg_file) as file:
        data = json.load(file)

    return data


async def get_season_id():
    """

    :return:
    """
    with open(pubg_file) as file:
        data = json.load(file)

    return data["season_id"]


async def get_last_update():
    """

    :return:
    """
    with open(pubg_file) as file:
        data = json.load(file)

    return data["last_update"]


async def get_account_id(player_name):
    """

    :return:
    """
    with open(pubg_file) as file:
        data = json.load(file)
    for user in data["users"]:
        if user["player_name"] == player_name:
            return user["account_id"]


# endregion


def takeSecond(elem):
    return elem[1]
