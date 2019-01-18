from config import config


min_played_match = config.config["min_played_match"]


async def get_ordered_table(players_stats, key_sort_list, is_average=True, reverse_sort=True, multiplier=1.0):
    """

    :return:
    """
    result = []

    for player in players_stats:
        played_match = players_stats[player].get("roundsPlayed")
        if played_match > int(min_played_match):
            if is_average:
                first_key = round(int(players_stats[player].get(key_sort_list[0])) / played_match, 2)
            else:
                first_key = players_stats[player].get(key_sort_list[0])

            second_key = players_stats[player].get(key_sort_list[1])
            third_key = players_stats[player].get(key_sort_list[2])
            result.append([player, first_key, second_key, third_key, multiplier])

    result.sort(key=lambda x: (x[1], x[2], x[3]), reverse=reverse_sort)
    print(result)
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

    players_table = []

    all_tables = []

    wins_average_table = await get_ordered_table(players_stats, ["wins", "top10s", "kills"], multiplier=3)
    all_tables.append(wins_average_table)

    wins_table = await get_ordered_table(players_stats, ["wins", "top10s", "kills"], is_average=False, multiplier=2)
    all_tables.append(wins_table)
    scores_table = await get_ordered_table(players_stats, ["rankPoints", "wins", "top10s"], is_average=False, multiplier=2)
    all_tables.append(scores_table)

    top10_average_table = await get_ordered_table(players_stats, ["top10s", "wins", "rankPoints"], multiplier=1.8)
    all_tables.append(top10_average_table)
    top10_table = await get_ordered_table(players_stats, ["top10s", "wins", "rankPoints"], is_average=False, multiplier=1.5)
    all_tables.append(top10_table)

    kills_average_table = await get_ordered_table(players_stats, ["kills", "wins", "rankPoints"], multiplier=1.7)
    all_tables.append(kills_average_table)
    kills_table = await get_ordered_table(players_stats, ["kills", "wins", "rankPoints"], is_average=False, multiplier=1.5)
    all_tables.append(kills_table)
    damages_average_table = await get_ordered_table(players_stats, ["damageDealt", "wins", "rankPoints"], multiplier=1.4)
    all_tables.append(damages_average_table)
    damages_table = await get_ordered_table(players_stats, ["damageDealt", "wins", "rankPoints"], is_average=False, multiplier=1.3)
    all_tables.append(damages_table)

    assist_average_table = await get_ordered_table(players_stats, ["assists", "wins", "rankPoints"], multiplier=1.3)
    all_tables.append(assist_average_table)
    assist_table = await get_ordered_table(players_stats, ["assists", "wins", "rankPoints"], is_average=False, multiplier=1.2)
    all_tables.append(assist_table)

    headshots_average_table = await get_ordered_table(players_stats, ["headshotKills", "wins", "rankPoints"], multiplier=1.2)
    all_tables.append(headshots_average_table)
    headshots_table = await get_ordered_table(players_stats, ["headshotKills", "wins", "rankPoints"], is_average=False, multiplier=1.2)
    all_tables.append(headshots_table)

    revives_average_table = await get_ordered_table(players_stats, ["revives", "wins", "rankPoints"], multiplier=1.5)
    all_tables.append(revives_average_table)
    revives_table = await get_ordered_table(players_stats, ["revives", "wins", "rankPoints"], is_average=False, multiplier=1)
    all_tables.append(revives_table)

    snipers_table = await get_ordered_table(players_stats, ["longestKill", "headshotKills", "wins"], is_average=False, multiplier=1)
    all_tables.append(snipers_table)

    played_match_table = await get_ordered_table(players_stats, ["roundsPlayed", "wins", "top10s"], is_average=False)
    most_kills_table = await get_ordered_table(players_stats, ["roundMostKills", "kills", "wins"], is_average=False)

    for player in players_stats:
        player_points = 0
        played_match = players_stats[player].get("roundsPlayed")
        player_wins = players_stats[player].get("wins")
        player_t10s = players_stats[player].get("top10s")
        player_kills = players_stats[player].get("kills")
        if played_match > int(min_played_match):
            for table in all_tables:
                player_points = player_points + await assign_points_to_player(player, table)

            players_table.append([player, player_points, player_wins, player_t10s, player_kills])

    players_table.sort(key=lambda x: (x[1]), reverse=True)

    return players_table


async def assign_points_to_player(player, table):
    """

    :param player:
    :param table:
    :param multiplier:
    :return:
    """
    players_count = len(table)
    i = 0
    for row in table:
        if row[0] == player:
            multiplier = row[4]
            actual_points_for_position = players_count - i + 1
            points = 10 * actual_points_for_position * multiplier
            return points
        i = i + 1

    return -10000


