from config import config


min_played_match = int(config.config["min_played_match"])


async def get_ordered_table(players_stats, key_sort_list, bia_multiplier, is_average=True, reverse_sort=True):
    """

    :return:
    """
    result = []
    bia_points = 0

    for player in players_stats:
        played_match = players_stats[player].get("roundsPlayed")
        if played_match > min_played_match:
            if is_average:
                first_key = round(int(players_stats[player].get(key_sort_list[0])) / played_match, 4)
                second_key = round(players_stats[player].get(key_sort_list[0]))
            else:
                first_key = round(players_stats[player].get(key_sort_list[0]))
                second_key = round(int(players_stats[player].get(key_sort_list[0])) / played_match, 4)

            #second_key = round(players_stats[player].get(key_sort_list[1]))
            third_key = round(players_stats[player].get(key_sort_list[1]))
            fourth_key = round(players_stats[player].get(key_sort_list[2]))
            fifth_key = round(players_stats[player].get(key_sort_list[3]))
            result.append([player, first_key, second_key, third_key, fourth_key, fifth_key, bia_points])

    result.sort(key=lambda x: (x[1], x[2], x[3], x[4], x[5]), reverse=reverse_sort)

    #assegnazione bia_points
    i = 0
    players_count = len(result)
    for row in result:
        actual_points_for_position = players_count - i + 1
        row[6] = 10 * actual_points_for_position * bia_multiplier
        i = i + 1

    return result


async def generate_all_tables(players_stats):
    """
    genera tutte le tabelle ordinate:
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

    played_match
    mostkills

    :param players_stats:
    :return:
    """

    best_players_table = []#[player, player_points, player_wins, player_t10s, played_match, player_kills]

    all_tables = []#[nometabella, tabella, moltiplicatore]

    #WINS
    keys_list = ["wins", "top10s", "rankPoints", "roundsPlayed"]
    wins_average_table = await get_ordered_table(players_stats, keys_list, 2.5)
    all_tables.append(["WINS_AV", wins_average_table])
    wins_table = await get_ordered_table(players_stats, keys_list, 2.2, is_average=False)
    all_tables.append(["WINS", wins_table])
    #SCORES
    keys_list = ["rankPoints", "wins", "top10s", "roundsPlayed"]
    scores_table = await get_ordered_table(players_stats, keys_list, 1, is_average=False)
    all_tables.append(["SCORES", scores_table])
    #TOP10
    keys_list = ["top10s", "wins", "rankPoints", "roundsPlayed"]
    top10_average_table = await get_ordered_table(players_stats, keys_list, 2)
    all_tables.append(["TOP10_AV", top10_average_table])
    top10_table = await get_ordered_table(players_stats, keys_list, 1.8, is_average=False)
    all_tables.append(["TOP10", top10_table])
    #KILLS
    keys_list = ["kills", "wins", "top10s", "roundsPlayed"]
    kills_average_table = await get_ordered_table(players_stats, keys_list, 1.7)
    all_tables.append(["KILLS_AV", kills_average_table])
    kills_table = await get_ordered_table(players_stats, keys_list, 1.5, is_average=False)
    all_tables.append(["KILLS", kills_table])
    #DAMAGE
    keys_list = ["damageDealt", "wins", "top10s", "roundsPlayed"]
    damages_average_table = await get_ordered_table(players_stats, keys_list, 1.3)
    all_tables.append(["DAMAGE_AV", damages_average_table])
    damages_table = await get_ordered_table(players_stats, keys_list, 1.2, is_average=False)
    all_tables.append(["DAMAGE", damages_table])
    #ASSISTS
    keys_list = ["assists", "wins", "top10s", "roundsPlayed"]
    assist_average_table = await get_ordered_table(players_stats, keys_list, 1.2)
    all_tables.append(["ASSISTS_AV", assist_average_table])
    assist_table = await get_ordered_table(players_stats, keys_list, 1, is_average=False)
    all_tables.append(["ASSISTS", assist_table])
    #HEADSHOTS
    keys_list = ["headshotKills", "wins", "top10s", "roundsPlayed"]
    headshots_average_table = await get_ordered_table(players_stats, keys_list, 1)
    all_tables.append(["HEADSHOTS_AV", headshots_average_table])
    headshots_table = await get_ordered_table(players_stats, keys_list, 0.8, is_average=False)
    all_tables.append(["HEADSHOTS", headshots_table])
    #REVIVES
    keys_list = ["revives", "wins", "top10s", "roundsPlayed"]
    revives_average_table = await get_ordered_table(players_stats, keys_list, 1)
    all_tables.append(["REVIVES_AV", revives_average_table])
    revives_table = await get_ordered_table(players_stats, keys_list, 0.8, is_average=False)
    all_tables.append(["REVIVES", revives_table])
    #SNIPERS
    keys_list = ["longestKill", "wins", "top10s", "roundsPlayed"]
    snipers_table = await get_ordered_table(players_stats, keys_list, 0.5, is_average=False)
    all_tables.append(["SNIPERS", snipers_table])
    #PLAYEDMATCH
    keys_list = ["roundsPlayed", "wins", "top10s", "kills"]
    played_match_table = await get_ordered_table(players_stats, keys_list, 1.5, is_average=False)
    all_tables.append(["PLAYEDMATCH", played_match_table])
    #MOSTKILLS
    keys_list = ["roundMostKills", "wins", "top10s", "roundsPlayed"]
    most_kills_table = await get_ordered_table(players_stats, keys_list, 0.5, is_average=False)
    all_tables.append(["MOSTKILLS", most_kills_table])

    for player in players_stats:
        player_points = 0
        played_match = players_stats[player].get("roundsPlayed")
        player_wins = players_stats[player].get("wins")
        player_t10s = players_stats[player].get("top10s")
        player_kills = players_stats[player].get("kills")
        if played_match > min_played_match:
            for table in all_tables:
                for row in table[1]:
                    if row[0] == player:
                        current_table_points = row[6]
                        player_points = player_points + current_table_points

            best_players_table.append([player, player_points, player_wins, player_t10s, player_kills, played_match])

    best_players_table.sort(key=lambda x: (x[1], x[2], x[3], x[4], x[5]), reverse=True)

    return [all_tables, best_players_table]


async def build_table():
    return


async def assign_points_to_player(player, table):
    """

    :param player:
    :param table:
    :param multiplier:
    :return:
    """
    players_count = len(table[1])
    multiplier = table[2]
    i = 0
    for row in table[1]:
        if row[0] == player:
            actual_points_for_position = players_count - i + 1
            points = 10 * actual_points_for_position * multiplier
            return points
        i = i + 1

    return -99000


