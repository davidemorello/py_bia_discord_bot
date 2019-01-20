import asyncio
import discord
import math
import random
import requests
from datetime import datetime
from discord import Game
from discord.ext.commands import Bot
from prettytable import PrettyTable

from config import config
from common import data_bot
from common import embed_data
from pubg import pubg_data

BOT_PREFIX = ('?', '!')
TOKEN = config.config['bot_token']
CSVFile = config.config['csvfile']
COLUMNS = ['ClientId', 'NomeUtente', 'DataRinnovo']

client = Bot(command_prefix=BOT_PREFIX)
discordClient = discord.Client()

"""
evento on_message non lo usiamo
@client.event
@asyncio.coroutine
async def on_message(message):
   if message.content.upper().startswith('?AAA'):
       if message.author.server_permissions.administrator:
           embed = discord.Embed(title='LeaderBoards', type="rich", description='Classifica', colour=0xDEADBF)
           #em.title("LeaderBoards")
           message_list = await pubg_data.print_leaderboards()
           i = 1
           for row in message_list:
               embed.set_author(name=message.author.name)
               embed.set_thumbnail(url=message.author.avatar_url)
               embed.add_field(name="#"+str(i), value=str(row[0]), inline=True)
               embed.add_field(name="-", value=str(row[1]), inline=True)
               i = i + 1
           await client.send_message(message.channel, embed=embed)
await dataBot.sync_users(message.server.members)
users = message.server.members
for user in users:
   print(str(user.id))
           print('ok')
users = client.get_all_members()
else:
   await client.say(str(context.message.author) + 'non hai i permessi per eseguire questo comando!')
elif message.content.upper().startswith('?E'):
  await edit_user_dataRinnovo({COLUMNS[0]: message.author.id, COLUMNS[1]: message.author, COLUMNS[2]:'10/10/9999'})
"""

"""
vittoria 25%
score 18%
top10 17%
killers 13%
damage 10%
assist 7%
medic 5%
cecchino 5%

<02:27:08> "=BIA= Maycool": vittoria 25%
top10 17%
score 15%
killers 13%
damage 13%
assist 7%
medic 5%
cecchino 5%

<02:29:29> "=BIA= Maycool": vittoria 25%
top10 20%
killers 17%
damage 15%
assist 10%
medic 8%
cecchino 6%

generate_main_players_table
"""


# region COMANDI PUBG
@client.command(pass_context=True)
async def pubg_best(context):
    #players_table = await pubg_data.generate_main_players_table()
    embed = await embed_data.embed_best_data()
    await client.say(embed=embed)


@client.command(pass_context=True)
async def pubg_lifetime(context, player_name):
    #stats = pubg_data.get_lifetime_player_stats(player_name)
    embed = await embed_data.embed_mylifetime_stats_data(player_name)
    await client.say(embed=embed)
    #await client.say(stats)


@client.command(pass_context=True)
async def test(context, player_name):
    """
    Solo per sviluppatori
    :param context:
    :param player_name:
    :return:
    """
    if context.message.author.server_permissions.administrator:
        players_stats = await pubg_data.get_all_players_stats()

        await pubg_data.get_winners(players_stats)
        return 0

        await pubg_data.get_bestboards(players_stats)
        return 0

        # client.send_message()
        em = discord.Embed(title='My Embed Title', description='My Embed Content.', colour=0xDEADBF)
        em.title("LeaderBoards")
        # em.add_field()
        await client.send_message(message.channel, embed=em)

        table = PrettyTable(['Nome', 'Score'])
        table.align = 'l'
        message_list = await pubg_data.print_leaderboards()
        for row in message_list:
            # print(row)
            table.add_row([row[0], str(round(row[1]))])
            num_points = "." * (20 - len(row[0]))
            # await client.say(len(num_points))
            # await client.say(row[0] + num_points + str(row[1]))

        print(table)
        await client.say(table)
        # await send_message_list(await pubg_data.print_leaderboards())

        # await(send_message_list(await pubg_stats_api.get_player_stats_temp()))
        # await pubg_stats_api.get_player_lifetime(playername)
        # await client.say(str(await pubg_stats_api.test()))

        # help(rsa)
        # for module in sys.modules:
        #   if('pycryptodome' in module):
        #      print(module)
        # Crypto.PublicKey.RSA.importKey.__getattribute__('')
        # auth = firebase.auth()
        # authenticate a user
        # user = auth.sign_in_with_email_and_password("mephisto980@gmail.com", "Qwerty12345")
        # print(str(user['idToken']))
        print(player_name)
        # userid = str(context.message.author.mention)
        # userid = await dataBot.CleanUserId(userid)
        # print(str(userid))
    else:
        await client.say("Solo per tester...")


@client.command(pass_context=True)
async def pubg_classifiche(context):
    """
    Stampa tutte le classifiche disponibili
    NO live
    :param context:
    :return:
    """
    embed = await embed_data.embed_legenda()
    await client.say(embed=embed)

    #players_stats = await pubg_data.get_all_players_stats()
    classifiche = await pubg_data.generate_all_classifiche()

    #classifica[0] ==> nome classifica
    #classifica[1] ==> classifica ordinata
    for classifica in classifiche:
        if classifica[0] == "WINS_AV":
            #embed = await embed_data.embed_win_av(classifica[1], '=== ' + str(classifica[0]) + ' ===')
            embed = await embed_data.embed_default(classifica[1], '=== ' + str(classifica[0]) + ' ===', 'Wins %', "T10s/S/K/P", is_average=True)
            await client.say(embed=embed)
        elif classifica[0] == "WINS":
            embed = await embed_data.embed_default(classifica[1], '=== ' + str(classifica[0]) + ' ===', 'Wins', "T10s/S/K/P")
            await client.say(embed=embed)
        elif classifica[0] == "SCORES":
            embed = await embed_data.embed_default(classifica[1], '=== ' + str(classifica[0]) + ' ===', "Score", "W/T10s/K/P")
            await client.say(embed=embed)
        elif classifica[0] == "TOP10_AV":
            embed = await embed_data.embed_default(classifica[1], '=== ' + str(classifica[0]) + ' ===', "top10 %", "W/S/K/P", is_average=True)
            await client.say(embed=embed)
        elif classifica[0] == "TOP10":
            embed = await embed_data.embed_default(classifica[1], '=== ' + str(classifica[0]) + ' ===', "top10", "W/S/K/P")
            await client.say(embed=embed)
        elif classifica[0] == "KILLS_AV":
            embed = await embed_data.embed_default(classifica[1], '=== ' + str(classifica[0]) + ' ===', "kills %", "W/T10s/D/P")
            await client.say(embed=embed)
        elif classifica[0] == "KILLS":
            embed = await embed_data.embed_default(classifica[1], '=== ' + str(classifica[0]) + ' ===', "kills", "W/T10s/D/P")
            await client.say(embed=embed)
        elif classifica[0] == "DAMAGE_AV":
            embed = await embed_data.embed_default(classifica[1], '=== ' + str(classifica[0]) + ' ===', "damage %", "W/T10s/K/P")
            await client.say(embed=embed)
        elif classifica[0] == "DAMAGE":
            embed = await embed_data.embed_default(classifica[1], '=== ' + str(classifica[0]) + ' ===', "damage", "W/T10s/K/P")
            await client.say(embed=embed)
        elif classifica[0] == "ASSISTS_AV":
            embed = await embed_data.embed_default(classifica[1], '=== ' + str(classifica[0]) + ' ===', "assists %", "W/T10s/K/P", is_average=True)
            await client.say(embed=embed)
        elif classifica[0] == "ASSISTS":
            embed = await embed_data.embed_default(classifica[1], '=== ' + str(classifica[0]) + ' ===', "assists", "W/T10s/K/P")
            await client.say(embed=embed)
        elif classifica[0] == "HEADSHOTS_AV":
            embed = await embed_data.embed_default(classifica[1], '=== ' + str(classifica[0]) + ' ===', "headshots %", "W/T10s/K/P", is_average=True)
            await client.say(embed=embed)
        elif classifica[0] == "HEADSHOTS":
            embed = await embed_data.embed_default(classifica[1], '=== ' + str(classifica[0]) + ' ===', "headshots", "W/T10s/K/P")
            await client.say(embed=embed)
        elif classifica[0] == "REVIVES_AV":
            embed = await embed_data.embed_default(classifica[1], '=== ' + str(classifica[0]) + ' ===', "revives %", "W/T10s/K/P", is_average=True)
            await client.say(embed=embed)
        elif classifica[0] == "REVIVES":
            embed = await embed_data.embed_default(classifica[1], '=== ' + str(classifica[0]) + ' ===', "revives", "W/T10s/K/P")
            await client.say(embed=embed)
        elif classifica[0] == "SNIPERS":
            embed = await embed_data.embed_default(classifica[1], '=== ' + str(classifica[0]) + ' ===', "sniper long kill", "W/T10s/K/P")
            await client.say(embed=embed)
        elif classifica[0] == "PLAYEDMATCH":
            embed = await embed_data.embed_default(classifica[1], '=== ' + str(classifica[0]) + ' ===', "played match", "W/T10s/K/S")
            await client.say(embed=embed)
        elif classifica[0] == "MOSTKILLS":
            embed = await embed_data.embed_default(classifica[1], '=== ' + str(classifica[0]) + ' ===', "most round kills", "W/T10s/K/P")
            await client.say(embed=embed)


@client.command(pass_context=True)
async def pubg_top10_live(context):
    """
    !LIVE!Sincronizza live i migliori 10 giocatori e stampa la leaderboard
    :param context:
    :return:
    """
    await client.say("Hai richiesto di visualizzare la lista dei migliori 10, è possibile eseguire questo comando"
                     " una volta ogni 60 secondi...")
    top10_list = await pubg_data.sync_top10_stats()

    embed = await embed_data.embed_top10_data(top10_list)
    # print(top10_list)
    await client.say(embed=embed)


@client.command(pass_context=True)
async def pubg_sync(context):
    """
    !LIVE!Attenzione! è possibile richiedere le stats LIVE 10 volte ogni 60 secondi,
    per cui i tempi della sincronizzazione ammontano a : numero di giocatori * 60 secondi
    NON mandare altri comandi fino alla fine della sincronizzazione.
    Aggiorna tutti i membri registrati con le stats in tempo reale
    :param context:
    :return:
    """
    await client.say("Sincronizzazione in corso, non mandare altri comandi fino alla fine della sincronizzazione...")
    await client.say("Tempo stimato : 120 secondi...")
    await client.say("...")
    await pubg_data.sync_pubg_players_stats()
    await client.say("Sincronizzazione completata!")


@client.command(pass_context=True)
async def pubg_mystats_live(context, player_name):
    """
    !LIVE!Comando : pubg_mylivestats <nick in pubg>
    Scrive le stats aggiornate in tempo reale dato un nick pubg
    :param context:
    :param player_name:
    :return:
    """
    await client.say("Hai richiesto di visualizzare le tue statistiche in tempo reale, vediamo quanto sei scarso! \n "
                     "Si prega di non spammare questo comando, è possibile eseguire richieste 10 volte ogni 60 secondi. \n "
                     "Grazie")

    embed = await embed_data.embed_mylivestats_data(player_name)
    await client.say(embed=embed)


@client.command(pass_context=True)
async def pubg_register(context, player_name):
    """
    !LIVE!Registrazione nuovo membro
    Comando: ?pubg_reg <nick_in_pubg>
    aggiorna anche le stats live
    :param context:
    :param player_name:
    :return:
    """
    message = await pubg_data.register_pubg_player(player_name)

    await client.say(str(message + player_name))
    players_stats = await pubg_data.get_all_players_stats()
    embed = await embed_data.embed_leaderboards_data(players_stats)
    await client.say(embed=embed)


@client.command(pass_context=True)
async def pubg_unregister(context, player_name):
    """
    Rimozione membro da statistiche
    :param context:
    :param player_name:
    :return:
    """
    message = await pubg_data.unregister_pubg_player(player_name)
    await client.say(message)
# endregion


# region COMANDI GESTIONE MEMBRI BIA - in lavorazione
@client.command(pass_context=True)
async def scaduti(context):
    """
    todo
    ritorna tutti i membri con common di rinnovo scaduta
    :param context:
    :return:
    """
    if context.message.author.server_permissions.administrator:
        await client.say('I seguenti membri hanno una common di rinnovo scaduta: ')
        dateNow = datetime.now()
        message = []
        userList = await data_bot.GetAllUsersFromCSV()
        for index in range(len(userList)):

            dataScadenza = str(userList[index][COLUMNS[2]])
            utenteCorrente = str(userList[index][COLUMNS[1]])

            datetime_object = datetime.strptime(dataScadenza, '%d/%m/%Y')

            if datetime_object < dateNow:
                message.append(str(utenteCorrente) + ' rinnovo scaduto il: ' + str(dataScadenza))

        # print('\n'.join(message))
        print(str(len(message)))
        print(str(math.ceil(len(message) / 30)))

        await send_message_list(message)

    else:
        await client.say(str(context.message.author) + ' non hai i permessi per eseguire questo comando!')


# discord ha un limite di lunghezza per ogni messaggio
async def send_message_list_pretty(messageList):
    max_rows_print = 30
    index = 0
    num_message_tosend = math.ceil(len(messageList) / max_rows_print)

    table = PrettyTable(['Nome', 'Score'])
    for i in range(0, num_message_tosend):
        if i == 0:
            index = max_rows_print
            table.add_row(messageList[i:i + max_rows_print])

        else:
            await client.say('\n'.join(messageList[index:index + max_rows_print]))
            index = index + max_rows_print

        await client.say(table)
        # print(str('i:'+str(i)+'  index:'+str(index) + '  ind+rows:' + str(max_rows_print+index)))
    await client.say('Fine')


# discord ha un limite di lunghezza per ogni messaggio
async def send_message_list(message_list):
    max_rows_print = 30
    index = 0
    num_message_tosend = math.ceil(len(message_list) / max_rows_print)

    for i in range(0, num_message_tosend):
        if i == 0:
            index = max_rows_print
            # row_string = messageList[i:i + max_rows_print][0] + '{0: >20}'.format(messageList[i:i + max_rows_print][1])
            await client.say('\n'.join(message_list[i:i + max_rows_print]))
        else:
            await client.say('\n'.join(message_list[index:index + max_rows_print]))
            index = index + max_rows_print
        # print(str('i:'+str(i)+'  index:'+str(index) + '  ind+rows:' + str(max_rows_print+index)))
    await client.say('Fine')


@client.command(pass_context=True)
async def prossime_scadenze(context):
    """
    todo
    ritorna i membri con scadenza inferiore a 1 mese
    :param context:
    :return:
    """
    if context.message.author.server_permissions.administrator:
        await client.say('I seguenti membri hanno una scadenza inferiore a 1 mese: ')
        dateNow = datetime.now()
        userList = await data_bot.GetAllUsersFromCSV()
        for index in range(len(userList)):

            data_scadenza = str(userList[index][COLUMNS[2]])
            utenteCorrente = str(userList[index][COLUMNS[1]])

            datetime_object = datetime.strptime(data_scadenza, '%d/%m/%Y')

            if (datetime_object > dateNow):
                giorni = datetime_object - dateNow
                # print(str(giorni.days))
                if (giorni.days < 31):
                    await client.say(utenteCorrente + ' scade il: ' + data_scadenza)

    else:
        await client.say(str(context.message.author) + ' non hai i permessi per eseguire questo comando!')


@client.command(pass_context=True)
async def conta_scaduti(context):
    """
    todo
    conta utenti con rinnovo scaduto
    :param context:
    :return:
    """
    count = await data_bot.count_user_delayed()
    await client.say('Numero membri con rinnovo scaduto: ' + count)


@client.command(pass_context=True)
async def scadenza_utente(context, userId):
    """
    todo
    dato un user ritorna la sua scadenza rinnovo
    :param context:
    :param userId:
    :return:
    """
    userId = await data_bot.CleanUserId(userId)
    userList = await data_bot.GetAllUsersFromCSV()
    user = ''
    for index in range(len(userList)):
        for key in userList[index]:
            if (str(userList[index][key]) == userId):
                await client.say(
                    str(context.message.mentions[0]) + ' Data Scadenza : ' + str(userList[index][COLUMNS[2]]))


@client.command(pass_context=True)
async def lista_bia(context):
    """
    todo
    lista di tutti i membri registrati nel sistema (csv)
    :param context:
    :return:
    """
    userList = await data_bot.GetAllUsersFromCSV()
    user = ''
    for index in range(len(userList)):
        await client.say(str(userList[index][COLUMNS[1]]) + ' Data Scadenza : ' + str(userList[index][COLUMNS[2]]))


@client.command(pass_context=True)
async def cancella(context, userId):
    """
    todo
    cancella un utente dal sistema (csv)
    :param context:
    :param userId:
    :return:
    """
    if context.message.author.server_permissions.administrator:
        userId = await data_bot.CleanUserId(userId)
        nomeUtente = str(context.message.mentions[0])
        print('Rimozione del membro: ' + nomeUtente)
        await data_bot.remove_user(userId)
        await client.say('Rimozione del membro: ' + nomeUtente + ' avvenuta correttamente')
    else:
        await client.say(str(context.message.author) + 'Non hai i permessi per eseguire questo comando!')


@client.command(pass_context=True)
async def rinnovo(context, userId, dataRinnovo):
    """
    todo
    rinnova common di rinnovo a un membro
    :param context:
    :param userId:
    :param dataRinnovo:
    :return:
    """
    if context.message.author.server_permissions.administrator:
        userId = await data_bot.CleanUserId(userId)
        nomeUtente = str(context.message.mentions[0])

        if not await data_bot.IsDataValid(dataRinnovo):
            await client.say('Data non valida! Utilizzare il seguente formato: gg/mm/aaaa.')
        else:
            print('Rinnovo common di scadenza del membro: ' + nomeUtente + ' nuova scadenza:' + dataRinnovo)
            print({COLUMNS[0]: userId, COLUMNS[1]: nomeUtente, COLUMNS[2]: dataRinnovo})
            await data_bot.edit_user_dataRinnovo({COLUMNS[0]: userId, COLUMNS[1]: nomeUtente, COLUMNS[2]: dataRinnovo})
            await client.say('Rinnovo common di scadenza del membro: ' + nomeUtente + ' nuova scadenza:' + dataRinnovo)
    else:
        await client.say(str(context.message.author) + 'Non hai i permessi per eseguire questo comando!')
# endregion


# region COMANDI DI TEST
@client.command(pass_context=True)
async def antani(context):
    """
    supercazzola
    :param context:
    :return:
    """
    possible_response = [
        'Con scappellamento a destra, per due',
        'Sbirigudi?',
        'Tarapìa tapiòco! Prematurata la supercazzola, o scherziamo?',
        'No, mi permetta. No, io... scusi, noi siamo in quattro. Come se fosse antani anche per lei soltanto in due, '
        'oppure in quattro anche scribàcchi confaldina? Come antifurto, per esempio',
        "No, aspetti, mi porga l'indice; ecco lo alzi così... guardi, guardi, guardi. Lo vede il dito? Lo vede che "
        "stuzzica? Che prematura anche? Ma allora io le potrei dire, anche con il rispetto per l'autorità, che anche "
        "soltanto le due cose come vicesindaco, capisce?",
        "Antani, come se fosse antani, anche per il direttore, la supercazzola con scappellamento.",
        "No, no, no, attenzione! Noo! Pàstene soppaltate secondo l'articolo 12, abbia pazienza, sennò posterdati, "
        "per due, anche un pochino antani in prefettura...",
        "...senza contare che la supercazzola prematurata ha perso i contatti col tarapìa tapiòco"
    ]

    await client.say(random.choice(possible_response) + ', ' + context.message.author.mention)


@client.command()
async def square(number):
    """
    dato un numero lo ritorna elevato alla potenza del numero stesso
    :param number:
    :return:
    """
    square_value = int(number) * int(number)
    await client.say(str(number) + ' square is ' + str(square_value))


@client.command()
async def d20():
    """
    tira un D20!
    :return:
    """
    await client.say(random.choice(range(1, 21)))


@client.command()
async def bitcoin():
    """
    Vuoi sapere il valore attuale del bitcoin (in $)? scoprilo
    :return:
    """
    url = 'https://api.coindesk.com/v1/bpi/currentprice/BTC.json'
    response = requests.get(url)
    value = response.json()['bpi']['USD']['rate']
    await client.say('Bitcoin price is : $ ' + value)
# endregion


# region BOT functions/events
async def list_servers():
    await client.wait_until_ready()
    while not client.is_closed:
        print('Current servers :')
        for server in client.servers:
            print(server.name)
        await asyncio.sleep(600)


@client.event
async def on_member_join(member):
    message = "Un nuovo utente si è unito al server: " + str(member)

    await client.send_message(discord.Object(id='527911773508993036'), message)
    await client.send_message(discord.Object(id='445234463383748640'), message)
    # mail_log_f(subject, string)


@client.event
async def on_ready():
    await client.change_presence(game=Game(name='fare il BOT'))
    await client.send_message(discord.Object(id='533011682428059649'), 'Eccomi sono di nuovo online!')
    await client.send_message(discord.Object(id='445234463383748640'), 'Eccomi sono di nuovo online!')
    print('Logged in as ' + client.user.name)

# @client.command(pass_context=True)
# async def t(context, userId):
#    userId = await cleanUserId(userId)
#    print(str(context.message.mentions[0]))
#    userTag = await GetNameTagByUserId(userId)
#    print(str(userTag))
#    await client.say('nametag = ' + str(userTag))

# endregion

client.loop.create_task(list_servers())

client.run(TOKEN)
