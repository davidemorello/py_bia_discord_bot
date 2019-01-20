import csv
from datetime import datetime
from config import config

CSVFile = config.config['csvfile']
COLUMNS = ['ClientId', 'NomeUtente', 'DataRinnovo']


# obsoleto non utilizzato
# dato userID (clientID) ritrova il suo nametag dal file csv
async def GetNameTagByUserId(userId):
    tag = ''
    userList = await GetAllUsersFromCSV()
    for index in range(len(userList)):
        for key in userList[index]:
            print('userid=' + userId + ' -- key=' + str(userList[index][key]))
            if (str(userList[index][key]) == userId):
                print('trovato :' + str(userList[index][key]))
                print('nomeutente :' + str(userList[index][COLUMNS[1]]))
                return str(userList[index][COLUMNS[1]])


# check validita formato dataRinnovo
async def IsDataValid(dataRinnovo):
    try:
        datetime_object = datetime.strptime(dataRinnovo, '%d/%m/%Y')
        # print(datetime_object.date())
        return True
    except:
        print('common non valida')
        return False


# quando menzionato, un user arriva con caratteri superflui e qui li puliamo es: <!@12334565678990>
async def CleanUserId(userId):
    # print('inizio pulizia userId')
    id = ''
    chars = '<>!@'
    for c in chars:
        if (c in userId):
            userId = userId.replace(c, '')

    # controllo che abbia 18 cifre
    # todo eccezione
    if (len(str(userId)) != 18):
        print('ERRORE pulizia userId ' + str(userId))

    print('fine pulizia userId :' + str(userId))
    return userId


# attenzione: da usare solo la prima volta - reset date rinnovo
async def sync_users(users):
    with open(CSVFile, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=COLUMNS)
        writer.writeheader()

        for user in users:
            print(user)
            writer.writerow({COLUMNS[0]: user.id, COLUMNS[1]: user, COLUMNS[2]: '01/01/1900'})


# edit common rinnovo user
async def remove_user(userId):
    usersList = await GetAllUsersFromCSV()
    isFound = False
    i = 0
    # ciclare lista ed editare il record con userid passato come parametro
    for row in usersList:
        if (row.get(COLUMNS[0]) == userId):  # .get(COLUMNS[0])):
            isFound = True
            usersList.remove(usersList[i])
            # usersList[i][COLUMNS[2]] = user.get(COLUMNS[2])
        i += 1

    # se non lo trova in lista bisogna aggiungerlo come nuovo record
    if (not isFound):
        return False

    mydict = {}
    ant = {}
    # apro csv e riscrivo tutti i dati che ho in pancia
    with open(CSVFile, 'w+', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=COLUMNS)
        writer.writeheader()
        for index in range(len(usersList)):
            # print(index)
            for key in usersList[index]:
                # print(key + ':'+ str(usersList[index][key]))
                ant.update({key: usersList[index][key]})

            mydict.update(ant)
            writer.writerow(mydict)


# edit common rinnovo user
async def count_user_delayed():
    usersList = await GetAllUsersFromCSV()
    print(str(len(usersList)))
    return str(len(usersList))


# edit common rinnovo user
async def edit_user_dataRinnovo(user):
    usersList = await GetAllUsersFromCSV()

    isFound = False
    i = 0
    # ciclare lista ed editare il record con userid passato come parametro
    for row in usersList:
        if (row.get(COLUMNS[0]) == user.get(COLUMNS[0])):
            isFound = True
            usersList[i][COLUMNS[2]] = user.get(COLUMNS[2])
        i += 1

    # se non lo trova in lista bisogna aggiungerlo come nuovo record
    if (not isFound):
        usersList.append(user)
        # usersList.append({COLUMNS[0]:user.get(COLUMNS[0])], [COLUMNS[1]:user.get(COLUMNS[1])], [COLUMNS[2]:user.get(COLUMNS[2])})

    mydict = {}
    ant = {}
    # apro csv e riscrivo tutti i dati che ho in pancia
    with open(CSVFile, 'w+', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=COLUMNS)
        writer.writeheader()
        for index in range(len(usersList)):
            # print(index)
            for key in usersList[index]:
                # print(key + ':'+ str(usersList[index][key]))
                ant.update({key: usersList[index][key]})

            mydict.update(ant)
            writer.writerow(mydict)


# Seleziona tutti gli utenti presi da csv
async def GetAllUsersFromCSV():
    usersList = []
    with open(CSVFile, 'r', newline='') as file:
        reader = csv.DictReader(file)

        for row in reader:
            usersList.append(row)

    return usersList


async def print_list_in_columns():
    i = 0
    return i

