import discord
from pubg import pubg_data


async def embed_legenda():
    embed = discord.Embed(title="LEGENDA", type="rich", colour=0xFF0000)
    last_update = await pubg_data.get_last_update()
    embed.description = "Stats aggiornate al: " + str(last_update)
    embed.add_field(name="W", value="WINS", inline=True)
    embed.add_field(name="T10", value="TOP 10", inline=True)
    embed.add_field(name="S", value="Score", inline=True)
    embed.add_field(name="K", value="Kills", inline=True)
    embed.add_field(name="D", value="Damage", inline=True)
    embed.add_field(name="P", value="Played Match", inline=True)

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
    embed = discord.Embed(title='=== TOP of the TOP ===', type="rich", colour=0xFF0000)
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
