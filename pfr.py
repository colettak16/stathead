# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
from bs4 import BeautifulSoup
import requests
from time import sleep
import xlsxwriter
from operator import itemgetter


GAMELOG_STATS = ["pass_cmp", "pass_att", "pass_cmp_pct", "pass_yds", "pass_td", "pass_int", "pass_rating", "pass_yds_per_att", "pass_adj_yds_per_att", "rush_att", "rush_yds", "rush_yds_per_att", "rush_td", "targets", "rec", "rec_yds", "rec_yds_per_rec", "rec_td", "catch_pct", "rec_yds_per_tgt", "all_td", "fumbles", "fumbles_lost"]
QB_STATS = ["qb_rec", "pass_cmp", "pass_att", "pass_cmp_pct", "pass_yds", "pass_td", "pass_td_perc", "pass_int", "pass_int_perc", "pass_first_down", "pass_long", "pass_yds_per_att", "pass_adj_yds_per_att", "pass_yds_per_cmp", "pass_yards_per_g", "pass_rating", "qbr", "pass_sacked", "pass_sacked_yds", "pass_net_yds_per_att", "pass_adj_net_yds_per_att", "pass_sacked_perc", "comebacks", "gwd", "av"]
WR_STATS = ["targets", "rec", "rec_yds", "rec_yds_per_rec", "rec_td", "rec_first_down", "rec_long", "rec_per_g", "rec_yds_per_g", "catch_pct", "rec_yds_per_tgt", "rush_att", "rush_yds", "rush_td", "rush_first_down", "rush_long", "rush_yds_per_att", "rush_yds_per_g", "rush_att_per_g", "touches", "yds_per_touch", "yds_from_scrimmage", "rush_receive_td", "fumbles", "av"]
RB_STATS = ["rush_att", "rush_yds", "rush_td", "rush_first_down", "rush_long", "rush_yds_per_att", "rush_yds_per_g", "rush_att_per_g", "targets", "rec", "rec_yds", "rec_yds_per_rec", "rec_td", "rec_first_down", "rec_long", "rec_per_g", "rec_yds_per_g", "catch_pct", "rec_yds_per_tgt", "touches", "yds_per_touch", "yds_from_scrimmage", "rush_receive_td", "fumbles", "av"]

baseUrl = 'https://www.pro-football-reference.com'


def promptMsg(statList):
    print("What type of stat(s) are you looking for?\nEnter the number(s) next to the stat, separated by commas, e.g.\n'4'\n'4, 7'\n'1, 3, 5'\n")
    for i in range(1, len(statList)+1):
        print(str(i) + ". " + statList[i-1])
    return input().split(", ")

def getStats(urlList, statList, tableList):
    mylist = []
    mylist2 = []
    stats = promptMsg(statList[0])
    i = 0
    for l in urlList:
        player = []
        r = requests.get(l)
        pageData = r.content
        soup = BeautifulSoup(pageData, 'lxml')
        table = soup.find("div", {"id" : tableList[i]})
        body = table.find("tbody")

        yn = "x"
        while (yn != 'Y' and yn != 'y' and yn !='N' and yn != 'n'):
            yn = "Y"
            if i > 0:
                msg = "Search different stats for " + PlayersWanted[i] + "? (Y/N)\n"
                yn = input(msg)
                if (yn != 'Y' and yn != 'y' and yn !='N' and yn != 'n'):
                    print("Invalid response, please try again")
            if ((yn == "Y" or yn == "y") and i > 0):
                stats = promptMsg(statList[i])

                
        for s in stats:
            asc = 'x'
            while (asc != 'A' and asc != 'a' and asc !='D' and asc != 'd'):
                if yn == "Y":
                    msg = "Should " + PlayersWanted[i] + " " + statList[i][int(s)-1] + " be sorted in ascending (A) or descending (D) order?\n"
                    asc = input(msg)
                    if (asc != 'A' and asc != 'a' and asc !='D' and asc != 'd'):
                        print("Invalid response, please try again")
                    
            statdata = []
            rows = body.find_all("tr", id=True)
            for d in rows:
                if tableList[i] == "all_stats":
                    date = d.find("td", {"data-stat" : "game_date"}).text
                else:
                    date = d.find("a").attrs['href'][-5:-1]
                cell = d.find("td", {"data-stat" : statList[i][int(s)-1]})
                if(cell.text and date):


                    ##ADD logic for cleaning cell.text with Record and CTCH% data to not fuck up my shit
                    if '%' in cell.text:
                        cell.text.replace('%', '')
                    if '-' in cell.text:
                        statdata.append((cell.text, date))
                    else:
                        statdata.append((float(cell.text), date))

            statname = PlayersWanted[i] + " " + statList[i][int(s)-1]
            mylist2.append(statname)

            resnum = 0
            if yn == "Y":
                while(resnum == 0):
                    msg = "Do you want all results to be shown? (Y/N)\n"
                    yn2 = input(msg)
                    if (yn2 == 'Y' or yn2 == 'y'):
                        resnum = len(statdata)
                    elif (yn2 == "N" or yn2 == 'n'):
                        msg = "How many results do you want to be shown?\n"
                        temp = int(input(msg))
                        if temp < resnum:
                            resnum = temp
                        else:
                            resnum = len(statdata)
                            print(PlayersWanted[i] + " does not have that many results, showing all data")
                    else:
                        print("Invalid response, please try again")

            if (asc == "a" or asc == 'a'):
                player.append(sorted(statdata, key=itemgetter(0))[0:resnum])
            else:
                player.append(sorted(statdata, key=itemgetter(0), reverse=True)[0:resnum])

        i += 1
        mylist.append(player)

    sn = 0
    for i in range(0, len(mylist)):
        for j in range(0, len(mylist[i])):
            print("Player/Stat: " + mylist2[sn])
            for e in mylist[i][j]:
                print(str(e[0]) + ", " + str(e[1]))
            sn += 1

def getPosition(url):
    r = requests.get(url)
    pageData = r.content
    soup = BeautifulSoup(pageData, 'lxml')
    info = soup.find("div", {"id" : "info"})
    return info.find_all("p")[1].text




while(True):
    msg = "What would you like to search for?\n1. Individual player stats\n2. Team Stats\n3. Stats Records\n4. Has anyone ever?\nOr type 'Done' to exit\n"
    TypeOfStat = input(msg)
    if TypeOfStat == '1':
        msg = "Which player(s) would you like to search for?\nEnter full player name(s), separated by commas, e.g.\n'Matthew Stafford'\n'Matthew Stafford, Aaron Rodgers'\n"
        PlayersWanted = input(msg).split(", ")
        playerlinks = []
        for v in PlayersWanted:
            #print(v)
            ln = v[v.find(' ') + 1]
            #print(ln)
            tempUrl = baseUrl+'/players/'+ln+'/'
            r = requests.get(tempUrl)
            pageData = r.content
            soup = BeautifulSoup(pageData, 'lxml')
            #print(soup)
            players = soup.find("div", {"id" : "div_players"})
            p2 = players.find_all("p")
            for p in p2:
                if v in p.text:
                    link = p.find("a").attrs['href']
                    break
            tempUrl = baseUrl + link
            playerlinks.append(tempUrl)

        msg = "1. Career High\\Low (Single Game)\n2. Career High\\Low (Full Season)\n3. Season High\\Low (Specific Year)\n4. Career Total\n5. Pro Bowl Years\n6. First-Team All Pro Years\n"
        GamevsSzn = input(msg)

        #SINGLE GAME CAREER DATA
        if GamevsSzn == '1':
            urlList = []
            statList = []
            tableList = []
            for l in playerlinks:
                tempUrl2 = l[0:len(l)-4] + "/gamelog/"
                urlList.append(tempUrl2)
                statList.append(GAMELOG_STATS)
                tableList.append("all_stats")
            getStats(urlList, statList, tableList)

        #SINGLE SEASON CAREER DATA
        elif GamevsSzn == '2':
            statList = []
            tableList = []
            for l in playerlinks:
                pos = getPosition(l)
                if "RB" in pos:
                    statList.append(RB_STATS)
                    tableList.append("all_rushing_and_receiving")
                elif "WR" in pos:
                    statList.append(WR_STATS)
                    tableList.append("all_receiving_and_rushing")
                else:
                    statList.append(QB_STATS)
                    tableList.append("all_passing")
            getStats(playerlinks, statList, tableList)

        #SINGLE GAME SEASON DATA
        elif GamevsSzn == '3':

            urlList = []
            statList = []
            tableList = []
            for l in playerlinks:
                tempUrl2 = l[0:len(l)-4] + "/gamelog/"
                urlList.append(tempUrl2)
                statList.append(GAMELOG_STATS)
                tableList.append("all_stats")
            getStats(urlList, statList, tableList)


        elif GamevsSzn == '4':
            pass
        elif GamevsSzn == '5':
            pass
        elif GamevsSzn == '6':
            pass
        else:
            print("Invalid response, please try again")





    elif TypeOfStat == '2':
        msg = "Which team would you like to search for?\n"
        TypeOfStat = input(msg)

    elif TypeOfStat == '3':
        msg = "Which record would you like to search for?\n"
        TypeOfStat = input(msg)

    elif TypeOfStat == '4':
        while(True):
            msg = "Which kind of filter would you like to add?\n1. Player Name Contains\n2.For specific team(s)\n3. Single Season Stat\n4. Single Game Stat\n5. Career Stat\n6.Career Time Frame"
            fltr = input(msg)

    elif TypeOfStat == 'Done' or TypeOfStat == 'done':
        break

    else:
        print("Not valid, please try again")







# #Build list of Stadium Names by URL
# stadiumNameDict = {}
# tempUrl = baseUrl+'/stadiums/'
# r = requests.get(tempUrl)
# pageData = r.content

# soup = BeautifulSoup(pageData,'lxml')
# table = soup.find_all('table')
# for tempTable in table:
#     for tableBody in tempTable.find_all('tbody'):
#         for rowdata in tableBody.find_all('tr'):
#             celldata = rowdata.find_all(['th','td'])[0]  #cell 0 will contain the Stadium Link
#             tempData = celldata.find_all('a',href=True)
#             if len(tempData) > 0:
#                 stadiumNameDict[tempData[0]['href']] = celldata.text


# ##Gamelog page is blocking me...
# ##Maybe read Passing Touchdowns instead?
                
# #Start with Career Passing TD Leaders
# tempUrl = baseUrl+'/leaders/pass_td_career.htm'
# r = requests.get(tempUrl)
# pageData = r.content

# #Find List of Players Name by reading Passing TD Leaders Table
# soup = BeautifulSoup(pageData,'lxml')
# table = soup.find_all('table')
# for tempTable in table:
#     for tableBody in tempTable.find_all('tbody'):
#         for rowdata in tableBody.find_all('tr'):
#             #This should be a player row...
#             celldata = rowdata.find_all(['th','td'])[1]
#             touchdownDict[celldata.text] = {}
#             tempData = celldata.find_all('a',href=True)
#             if len(tempData) > 0:
#                 touchdownDict[celldata.text]['url'] = tempData[0]['href']

# #Dictionary to correlate Game URLs with their Stadium
# gameStadiumDict = {}

# #For Each Player, Go to their Passing TD Log and Go through each TD, picking out 
# #stadiums they occurred in

# for player in touchdownDict.keys():
#     print('Researching '+player)
#     tempUrl = baseUrl+touchdownDict[player]['url'][:-4]+'/touchdowns/passing'
#     r = requests.get(tempUrl)
#     pageData = r.content
    
#     soup = BeautifulSoup(pageData,'lxml')
#     table = soup.find_all('table')
#     #Table now contains 9 or 10 tables.  table[8] is Reg Season, table[9] Post Season
#     for tempTable in table:
#         for tableBody in tempTable.find_all('tbody'):
#             #Only Reg and Post Season Tables have 'tbody'
#             for rowdata in tableBody.find_all('tr'):            
#                 celldata = rowdata.find_all(['th','td'])[2]  #cell 2 will contain the game link
#                 tempData = celldata.find_all('a',href=True)
#                 if len(tempData) > 0:
#                     tempGameUrl = baseUrl+tempData[0]['href']
                    
#                     #Don't need to scrape pages for games we've already found...
#                     if not tempGameUrl in gameStadiumDict:
#                         hasStadium = 0
#                         #Go Find stadium for this game
#                         r = requests.get(tempGameUrl)
#                         tempGameSoup = BeautifulSoup(r.content,'lxml')
#                         tempGameData = tempGameSoup.find_all('div',class_='scorebox_meta')[0]
#                         tempData = tempGameData.find_all('div')
#                         for tempLine in tempData:
#                             if repr(tempLine).find('Stadium') != -1:
#                                 tempStadium = tempLine.find_all('a',href=True)
#                                 gameStadiumDict[tempGameUrl] = tempStadium[0]['href']
#                                 hasStadium = 1
#                     else:
#                          hasStadium = 1           
                                    
#                     if hasStadium:
#                         #Extract Stadium Name
#                         tempStadium = stadiumNameDict[gameStadiumDict[tempGameUrl]]
#                     else:
#                         #Skip this game
#                         continue
                    
#                     #Make sure there is a value in the dictionary
#                     if not tempStadium in touchdownDict[player]:
#                         touchdownDict[player][tempStadium] = 0
                    
#                     #Increment TD in given Stadium
#                     touchdownDict[player][tempStadium] = touchdownDict[player][tempStadium] + 1
          
# #Create xlsx file to write data into
# fileName = 'C:\\My Stuff\\scrapepfr.xlsx'
# xbook = xlsxwriter.Workbook(fileName)
# xsheet = xbook.add_worksheet('Sheet 1')

# #Row Index
# rowNum = 0

# stadiumNames = []
# for key in stadiumNameDict.keys():
#     stadiumNames.append(stadiumNameDict[key])

# #Write Stadium Names as Column Headers
# xsheet.write_row(rowNum,0,['Player Name'])
# xsheet.write_row(rowNum,1,stadiumNames)
# rowNum = rowNum + 1

# for player in touchdownDict.keys():
#     #Write Player Name
#     xsheet.write_row(rowNum,0,[player])
    
#     for stadium in touchdownDict[player].keys():
#         if stadium == 'url':
#             #Skip this entry
#             continue

#         #Write the parameters that we found into our spreadsheet
#         if stadium in stadiumNames:
#             colIndex = stadiumNames.index(stadium)+1 #Shift by 1 to account for Player Name Column
#             xsheet.write_row(rowNum,colIndex,[touchdownDict[player][stadium]])
#         else:
#             print('Unknown Stadium - '+stadium)
        
#     #Increment rowNum and close the file
#     rowNum = rowNum + 1

# xbook.close()