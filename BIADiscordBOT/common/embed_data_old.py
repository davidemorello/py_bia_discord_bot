import discord
from pubg import pubg_data


async def embed_win_av(players_table, title):
    embed = discord.Embed(title=title, type="rich", colour=0xDEADBF)
    last_update = await pubg_data.get_last_update()
    embed.description = "Statistiche aggiornate al: " + str(last_update)
    name = ''
    main = ''
    extras = ''
    i = 1
    for row in players_table:
        #print(row)
        name += str(i) + ". " + row[0] + '\n'
        main += str(round(float(row[1]) * 100, 2)) + "%" + '\n'
        extras += str(row[1]) + "/" + str(row[2]) + "/" + str(row[3]) + str(row[4]) + '\n'
        i = i + 1

    embed.add_field(name="Nick", value=name, inline=True)
    embed.add_field(name="Wins%", value=main, inline=True)
    embed.add_field(name="W/T10/P", value=extras, inline=True)

    return embed


async def embed_win(players_table, title):
    embed = discord.Embed(title=title, type="rich", colour=0xDEADBF)
    last_update = await pubg_data.get_last_update()
    embed.description = "Statistiche aggiornate al: " + str(last_update)
    name = ''
    main = ''
    extras = ''
    i = 1
    for row in players_table:
        #print(row)
        name += str(i) + ". " + row[0] + '\n'
        main += str(row[1]) + '\n'
        extras += str(row[1]) + "/" + str(row[2]) + "/" + str(row[3]) + '\n'
        i = i + 1

    embed.add_field(name="Nick", value=name, inline=True)
    embed.add_field(name="Wins", value=main, inline=True)
    embed.add_field(name="W/T10/P", value=extras, inline=True)

    return embed


async def embed_score(players_table, title):
    embed = discord.Embed(title=title, type="rich", colour=0xDEADBF)
    last_update = await pubg_data.get_last_update()
    embed.description = "Statistiche aggiornate al: " + str(last_update)
    name = ''
    main = ''
    extras = ''
    i = 1
    for row in players_table:
        #print(row)
        name += str(i) + ". " + row[0] + '\n'
        main += str(round(row[1])) + '\n'
        extras += str(row[2]) + "/" + str(row[3]) + "/" + str(row[4]) + '\n'
        i = i + 1

    embed.add_field(name="Nick", value=name, inline=True)
    embed.add_field(name="Score", value=main, inline=True)
    embed.add_field(name="W/T10/P", value=extras, inline=True)

    return embed


async def embed_default(players_table, title, description, headers, colour=0xDEADBF, is_average=False):
    embed = discord.Embed(title=title, description=description, type="rich", colour=colour)
    #last_update = await pubg_data.get_last_update()
    name = ''
    main = ''
    extras = ''
    i = 1
    for row in players_table:
        name += str(i) + ". " + row[0] + '\n'
        if is_average:
            main += str(round(row[1] * 100, 2)) + '\n'
        else:
            main += str(round(row[1], 2)) + '\n'
        extras += str(row[2]) + "/" + str(row[3]) + "/" + str(row[4]) + "/" + str(row[5]) + '\n'
        i = i + 1

    embed.add_field(name="Nick", value=name, inline=True)
    embed.add_field(name=description, value=main, inline=True)
    embed.add_field(name=headers, value=extras, inline=True)

    return embed


async def embed_best_data():
    embed = discord.Embed(title='=== TOP of the TOP ===', type="rich", colour=0xDEADBF)
    last_update = await pubg_data.get_last_update()
    embed.description = "Statistiche aggiornate al: " + str(last_update)
    players_table = await pubg_data.generate_main_players_table()
    name = ''
    main = ''
    extras = ''
    i = 1
    for row in players_table:
        name += str(i) + ". " + row[0] + '\n'
        main += str(round(row[1])) + '\n'
        extras += str(row[2]) + "/" + str(row[3]) + "/" + str(row[4]) + "/" + str(row[5]) + '\n'
        i = i + 1

    embed.add_field(name="Nick", value=name, inline=True)
    embed.add_field(name="Score", value=main, inline=True)
    embed.add_field(name="W/T10/P/K", value=extras, inline=True)

    return embed


async def embed_top10_data(top10_list):
    embed = discord.Embed(title='=== TOP 10 ===', description='Solo i migliori', type="rich", colour=0xDEADBF)
    name = ''
    score = ''
    wtp = ''
    i = 1
    for row in top10_list:
        name += str(i) + ". " + row[0] + '\n'
        score += str(row[1].get("rankPoints")) + '\n'
        wtp += str(row[1].get("wins")) + "/" + str(row[1].get("top10s")) + "/" + str(row[1].get("roundsPlayed")) + '\n'
        # embed.set_author(name=context.message.author.name)
        # embed.set_thumbnail(url=context.message.author.avatar_url)
        i = i + 1

    embed.add_field(name="Nick", value=name, inline=True)
    embed.add_field(name="Score", value=score, inline=True)
    embed.add_field(name="W/T10/P", value=wtp, inline=True)
    return embed


async def embed_bestboards_data(players_stats):
    embed = discord.Embed(title='=== CLASSIFICA GENERALE ===',
                          description="Classifica in base alla media delle posizioni nelle diverse classifiche \n"
                                      "NB: rientra nelle classifiche solo chi ha completato almeno 20 partite",
                          type="rich", colour=0xDEADBF)
    message_list = await pubg_data.get_bestboards(players_stats)
    name = ''
    media_pos = ''
    best_for = ''
    i = 1
    for row in message_list:
        name += str(i) + ". " + row[0] + '\n'
        media_pos += str(row[1]) + '\n'
        best_for += str(row[2]) + '\n'
        i = i + 1

    embed.add_field(name="Nick", value=name, inline=True)
    embed.add_field(name="Media", value=media_pos, inline=True)
    embed.add_field(name="Awards", value=best_for, inline=True)

    return embed


async def embed_assistboards_data(players_stats):
    embed = discord.Embed(title='=== THE ASSISTMAN ===', type="rich", colour=0xDEADBF)
    message_list = await pubg_data.get_board(players_stats, "assists", ["assists", "revives", "teamKills"])
    name = ''
    main = ''
    extras = ''
    i = 1
    for row in message_list:
        name += str(i) + ". " + row[0] + '\n'
        main += str(round(row[1],2)) + '\n'
        extras += str(row[2]) + '\n'
        i = i + 1

    embed.add_field(name="Nick", value=name, inline=True)
    embed.add_field(name="Assist (media)", value=main, inline=True)
    embed.add_field(name="Assist/Revive/TeamKills", value=extras, inline=True)

    return embed


async def embed_damageboards_data(players_stats):
    embed = discord.Embed(title='=== THE DEMOLISHER ===', type="rich", colour=0xDEADBF)
    message_list = await pubg_data.get_board(players_stats, "damageDealt", ["damageDealt", "kills", "roundMostKills"])
    name = ''
    main = ''
    extras = ''
    i = 1
    for row in message_list:
        name += str(i) + ". " + row[0] + '\n'
        main += str(round(row[1])) + '\n'
        extras += str(row[2]) + '\n'
        i = i + 1

    embed.add_field(name="Nick", value=name, inline=True)
    embed.add_field(name="Danni (media)", value=main, inline=True)
    embed.add_field(name="Danni/Kills/Most Kills", value=extras, inline=True)

    return embed


async def embed_killerboards_data(players_stats):
    embed = discord.Embed(title='=== THE KILLERS ===', type="rich", colour=0xDEADBF)
    message_list = await pubg_data.get_board(players_stats, "kills", ["kills", "headshotKills", "damageDealt"])
    name = ''
    kd = ''
    khd = ''
    i = 1
    for row in message_list:
        name += str(i) + ". " + row[0] + '\n'
        kd += str(round(row[1],2)) + '\n'
        khd += str(row[2]) + '\n'
        i = i + 1

    embed.add_field(name="Nick", value=name, inline=True)
    embed.add_field(name="KD", value=kd, inline=True)
    embed.add_field(name="Kills/HeadShots/Damage", value=khd, inline=True)

    return embed


async def embed_leaderboards_data(players_stats):
    embed = discord.Embed(title='=== LEADERBOARDS ===', type="rich", colour=0xDEADBF)
    # em.title("LeaderBoards")
    message_list = await pubg_data.get_board(players_stats, "rankPoints", ["wins", "top10s", "roundsPlayed"], False)
    name = ''
    score = ''
    wtp = ''
    i = 1
    for row in message_list:
        name += str(i) + ". " + row[0] + '\n'
        score += str(round(row[1])) + '\n'
        wtp += str(row[2]) + '\n'
        # embed.set_author(name=context.message.author.name)
        # embed.set_thumbnail(url=context.message.author.avatar_url)
        i = i + 1

    embed.add_field(name="Nick", value=name, inline=True)
    embed.add_field(name="Score", value=score, inline=True)
    embed.add_field(name="Wins/Top10/Played", value=wtp, inline=True)
    return embed


async def embed_winnerboards_data(players_stats):
    embed = discord.Embed(title='=== THE CHICKEN WINNERS ===', type="rich", colour=0xDEADBF)
    # em.title("LeaderBoards")
    message_list = await pubg_data.get_board(players_stats, "wins", ["wins", "top10s", "roundsPlayed"])
    name = ''
    wins_perc = ''
    wtp = ''
    i = 1
    for row in message_list:
        name += str(i) + ". " + row[0] + '\n'
        wins_perc += str(round(row[1]*100, 2)) + "%" + '\n'
        wtp += str(row[2]) + '\n'
        # embed.set_author(name=context.message.author.name)
        # embed.set_thumbnail(url=context.message.author.avatar_url)
        i = i + 1

    embed.add_field(name="Nick", value=name, inline=True)
    embed.add_field(name="Wins%", value=wins_perc, inline=True)
    embed.add_field(name="Wins/Top10/Played", value=wtp, inline=True)
    return embed


async def embed_medicboards_data(players_stats):
    embed = discord.Embed(title='=== THE MEDICS ===', type="rich", colour=0xDEADBF)
    # em.title("LeaderBoards")
    message_list = await pubg_data.get_board(players_stats, "revives", ["revives", "assists", "teamKills"])
    name = ''
    revives_perc = ''
    wtp = ''
    i = 1
    for row in message_list:
        name += str(i) + ". " + row[0] + '\n'
        revives_perc += str(round(row[1]*100,2)) + "%" + '\n'
        wtp += str(row[2]) + '\n'
        # embed.set_author(name=context.message.author.name)
        # embed.set_thumbnail(url=context.message.author.avatar_url)
        i = i + 1

    embed.add_field(name="Nick", value=name, inline=True)
    embed.add_field(name="Revives%", value=revives_perc, inline=True)
    embed.add_field(name="Revives/Assists/TeamKill", value=wtp, inline=True)
    return embed


async def embed_sniperboards_data(players_stats):
    embed = discord.Embed(title='=== THE SNIPERS ===', type="rich", colour=0xDEADBF)
    # em.title("LeaderBoards")
    message_list = await pubg_data.get_board(players_stats, "longestKill", ["headshotKills", "kills", "damageDealt"], ismean=False)
    name = ''
    long_kill = ''
    hkd = ''
    i = 1
    for row in message_list:
        name += str(i) + ". " + row[0] + '\n'
        long_kill += str(round(row[1], 2)) + '\n'
        hkd += str(row[2]) + '\n'
        # embed.set_author(name=context.message.author.name)
        # embed.set_thumbnail(url=context.message.author.avatar_url)
        i = i + 1

    embed.add_field(name="Nick", value=name, inline=True)
    embed.add_field(name="Longest Kill(m)", value=long_kill, inline=True)
    embed.add_field(name="HeadShots/Kills/Damage", value=hkd, inline=True)
    return embed


async def embed_mylivestats_data(player_name):
    embed = discord.Embed(title='=== QUANTO SONO SCARSO ? ===', type="rich", colour=0xDEADBF)
    player_data = await pubg_data.get_live_player_detail(player_name)
    print(player_data[player_name])
    name = player_name
    stats = ''

    for row in player_data[player_name]:
        stat_name = row
        stat_value = player_data[player_name][row]
        stats += str(stat_name) + ": " + str(stat_value) + '\n'

    embed.add_field(name=name, value=stats, inline=True)

    return embed


async def embed_mylifetime_stats_data(player_name):
    embed = discord.Embed(title='=== LIFETIME ===', type="rich", colour=0xDEADBF)
    player_data = await pubg_data.get_lifetime_player_stats(player_name)
    print(player_data[player_name])
    name = player_name
    stats = ''

    for row in player_data[player_name]:
        stat_name = row
        stat_value = player_data[player_name][row]
        stats += str(stat_name) + ": " + str(stat_value) + '\n'

    embed.add_field(name=name, value=stats, inline=True)

    return embed
