from config import config
from pubg import pubg_stats_api
import json
from time import sleep
import asyncio
import numpy
from pubg import pubg_rank_generator

pubg_file = config.config['pubg_file']
pubg_player_stats = config.config['pubg_player_stats']
min_played_games = 10


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
    return players_table


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


async def genera_classifica_generale(players_stats):
    """
    WIN% x3

    WINs x2.1 30
    Score x1.9 40

    Top10% x1.6
    top10 x1.7

    kills%  x1.4 18
    kills   x1.3
    damage% x1.2
    damage  x1.1

    assist% x0.59
    hs% x0.57
    headshots  x0.53
    assist x0.52
    revive% x0.51

    medic(revive) x0.35
    sniper(longkill) x 0.3

    :return:
    """
    wins_perc_ranks = await get_board(players_stats, "wins", ["wins", "top10s", "roundsPlayed"], False)
    wins_ranks = await get_board(players_stats, "wins", ["wins", "top10s", "roundsPlayed"], False)

    scores = await get_leaderboards(players_stats)
    killers = await get_killerboards(players_stats)
    medics = await get_assistboards(players_stats)
    winners = await get_winnerboards(players_stats)
    snipers = await get_sniperboards(players_stats)
    damages = await get_damageboards(players_stats)

    bestboards = []

    # calcolo media posizione di ogni classifica per ogni player e la ordino (media minore)
    for player in scores:
        player_positions = [
            await get_position(scores, player[0]),
            await get_position(killers, player[0]),
            await get_position(medics, player[0]),
            await get_position(winners, player[0]),
            await get_position(snipers, player[0])
        ]
        pos_media = numpy.mean(player_positions)
        best_for = ""

        if 1 in player_positions:
            if player_positions[0] == 1:
                best_for += "Best Score "
            if player_positions[1] == 1:
                best_for += "Best Killer "
            if player_positions[2] == 1:
                best_for += "Best Medic "
            if player_positions[3] == 1:
                best_for += "Best Winner "
            if player_positions[4] == 1:
                best_for += "Best Sniper "

        bestboards.append([player[0], pos_media, best_for])

    bestboards.sort(key=takeSecond, reverse=False)
    print(bestboards)
    return bestboards


async def get_bestboards(players_stats):
    """

    :return:
    """

    scores = await get_leaderboards(players_stats)
    killers = await get_killerboards(players_stats)
    medics = await get_assistboards(players_stats)
    winners = await get_winnerboards(players_stats)
    snipers = await get_sniperboards(players_stats)

    bestboards = []

    # calcolo media posizione di ogni classifica per ogni player e la ordino (media minore)
    for player in scores:
        player_positions = [
            await get_position(scores, player[0]),
            await get_position(killers, player[0]),
            await get_position(medics, player[0]),
            await get_position(winners, player[0]),
            await get_position(snipers, player[0])
        ]
        pos_media = numpy.mean(player_positions)
        best_for = ""

        if 1 in player_positions:
            if player_positions[0] == 1:
                best_for += "Best Score "
            if player_positions[1] == 1:
                best_for += "Best Killer "
            if player_positions[2] == 1:
                best_for += "Best Medic "
            if player_positions[3] == 1:
                best_for += "Best Winner "
            if player_positions[4] == 1:
                best_for += "Best Sniper "

        bestboards.append([player[0], pos_media, best_for])

    bestboards.sort(key=takeSecond, reverse=False)
    print(bestboards)
    return bestboards


async def get_position(board, player_name):
    index = 1
    for item in board:
        if item[0] == player_name:
            return index
        index = index + 1


async def get_board(players_stats, main_field, list_extra, ismean=True):
    """

    :return:
    """
    players_data = []

    for player in players_stats:
        rounds_played = int(players_stats[player].get("roundsPlayed"))
        if rounds_played > min_played_games:
            if ismean:
                main = round(int(players_stats[player].get(main_field)) / rounds_played, 2)
            else:
                main = players_stats[player].get(main_field)

            extras = "{0}/{1}/{2}".format(str(players_stats[player].get(list_extra[0])),
                                          str(players_stats[player].get(list_extra[1])),
                                          str(round(players_stats[player].get(list_extra[2]))))

            players_data.append([player, main, extras])

    players_data.sort(key=takeSecond, reverse=True)

    return players_data


async def get_winners(players_stats):
    """

       :return:
       """
    players_wins = []

    for player in players_stats:
        if players_stats[player].get("roundsPlayed") > min_played_games:
            wins = players_stats[player].get("wins")
            #wins_perc = round(wins / players_stats[player].get("roundsPlayed") * 100, 2)
            top10 = players_stats[player].get("top10s")
            players_wins.append([player, wins, top10])

    players_wins.sort(key=lambda x: (x[1], x[2]), reverse=True)
    print(players_wins)
    return players_wins


# region METODI Sostituiti con uno generico ==> get_board(...)

async def get_killerboards(players_stats):
    """

    :return:
    """
    # players_stats = await get_all_players_stats()
    players_killers = []

    for player in players_stats:
        if int(players_stats[player].get("roundsPlayed")) > min_played_games:
            kd = round(int(players_stats[player].get("kills")) / int(players_stats[player].get("roundsPlayed")), 2)
            khd = "{0}/{1}/{2}".format(str(players_stats[player].get("kills")),
                                       str(players_stats[player].get("headshotKills")),
                                       str(round(players_stats[player].get("damageDealt"))))

            players_killers.append([player, kd, khd])

    players_killers.sort(key=takeSecond, reverse=True)

    return players_killers


async def get_leaderboards(players_stats):
    """

    :return:
    """
    # players_stats = await get_all_players_stats()
    players_scores = []

    for player in players_stats:
        if int(players_stats[player].get("roundsPlayed")) > min_played_games:
            score = str(round(players_stats[player].get("rankPoints")))
            wtp = '{0}/{1}/{2}'.format(str(players_stats[player].get("wins")),
                                       str(players_stats[player].get("top10s")),
                                       str(players_stats[player].get("roundsPlayed")))
            players_scores.append([player, score, wtp])

    players_scores.sort(key=takeSecond, reverse=True)

    return players_scores


async def get_damageboards(players_stats):
    """

    :return:
    """
    # players_stats = await get_all_players_stats()
    players_scores = []

    for player in players_stats:
        if int(players_stats[player].get("roundsPlayed")) > min_played_games:
            dmg_perc = round(players_stats[player].get("damageDealt") / players_stats[player].get("roundsPlayed"))
            # score = str(round(players_stats[player].get("damageDealt")))
            wtp = "{0}/{1}/{2}".format(str(round(players_stats[player].get("damageDealt"))),
                                       str(players_stats[player].get("kills")),
                                       str(players_stats[player].get("roundMostKills")))
            players_scores.append([player, dmg_perc, wtp])

    players_scores.sort(key=takeSecond, reverse=True)

    return players_scores


async def get_assistboards(players_stats):
    """

    :return:
    """
    # players_stats = await get_all_players_stats()
    players_scores = []

    for player in players_stats:
        if int(players_stats[player].get("roundsPlayed")) > min_played_games:
            assists = round(players_stats[player].get("assists") / players_stats[player].get("roundsPlayed"), 2)
            # score = str(round(players_stats[player].get("damageDealt")))
            wtp = str(round(players_stats[player].get("assists"))) + "/" + str(
                players_stats[player].get("revives")) + "/" + str(players_stats[player].get("teamKills"))
            players_scores.append([player, assists, wtp])

    players_scores.sort(key=takeSecond, reverse=True)

    return players_scores



async def get_winnerboards(players_stats):
    """

    :return:
    """
    # players_stats = await get_all_players_stats()
    players_scores = []

    for player in players_stats:
        if players_stats[player].get("roundsPlayed") > min_played_games:
            wins = players_stats[player].get("wins")
            wins_perc = round(wins / players_stats[player].get("roundsPlayed") * 100, 2)
            wtp = str(wins) + "/" + str(players_stats[player].get("top10s")) + "/" + str(
                players_stats[player].get("roundsPlayed"))
            players_scores.append([player, wins_perc, wtp])

    players_scores.sort(key=takeSecond, reverse=True)

    return players_scores


async def get_medicboards(players_stats):
    """

    :return:
    """
    # players_stats = await get_all_players_stats()
    players_scores = []

    for player in players_stats:
        if players_stats[player].get("roundsPlayed") > min_played_games:
            revives = players_stats[player].get("revives")
            revives_perc = round(revives / players_stats[player].get("roundsPlayed") * 100, 2)
            wtp = str(revives) + "/" + str(players_stats[player].get("assists")) + "/" + str(
                players_stats[player].get("teamKills"))
            players_scores.append([player, revives_perc, wtp])

    players_scores.sort(key=takeSecond, reverse=True)

    return players_scores


async def get_sniperboards(players_stats):
    """

    :return:
    """
    # players_stats = await get_all_players_stats()
    players_scores = []

    for player in players_stats:
        if int(players_stats[player].get("roundsPlayed")) > min_played_games:
            long_kill = players_stats[player].get("longestKill")
            hkd = str(players_stats[player].get("headshotKills")) + "/" + str(
                players_stats[player].get("kills")) + "/" + str(round(players_stats[player].get("damageDealt")))
            players_scores.append([player, long_kill, hkd])

    players_scores.sort(key=takeSecond, reverse=True)

    return players_scores
# endregion

# endregion


# region GET common LOCAL
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
