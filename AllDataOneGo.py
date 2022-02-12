import requests
from bs4 import BeautifulSoup as bs
import csv
from selenium import webdriver

transfer_list = {}
year_list = ['2020','2019','2018','2017','2016','2015']

for year in year_list:    
    URL_allschool = "https://www.sports-reference.com/cbb/seasons/" + year + "-school-stats.html"
    page = requests.get(URL_allschool)
    soup = bs(page.content, "html.parser")
    table = soup.find_all("table")
    teams_table = table[0]
    teams = teams_table.find_all("a")
    team_list = []

    for team in teams:
        team = str(team)
        team = team.lstrip('<a href="')
        team = team.split('">')
        team = ('https://www.sports-reference.com' + team[0])
        team_list.append(team)

    player_list = {}
    
    for team in team_list:
        page = requests.get(team)
        soup = bs(page.content, "html.parser")
        table = soup.find_all("table")
        player_table = table[0]
        players = player_table.find_all("a")
        for player in players:
            player = str(player)
            player = player.lstrip('<a href="')
            player = player.split('">')
            player = ('https://www.sports-reference.com' + player[0])
            player_list[player] = '', ''


    for player in player_list:
        page = requests.get(player)
        soup = bs(page.content, "html.parser")
        name = soup.find('h1').text
        name = name.strip()
        schools = soup.find('p')
        schools = schools.text.split('\n')
        for school in schools:
            if "Schools: " in school:
                schools_seperated = []
                try:
                    school = school[9:]
                    school = school.split(' and ')
                    if ',' in school[0]:
                        two_schools = school[0].split(', ')
                        schools_seperated.extend([two_schools[0],two_schools[1],school[1]])
                    else:
                        schools_seperated.extend([school[0],school[1]])
                    if len(schools_seperated) == 2:
                        transfer_list[name] = [player, schools_seperated[0], schools_seperated[1]]
                    else:
                        transfer_list[name] = [player, schools_seperated[0], schools_seperated[1]]
                        transfer_list[name + '2'] = [player, schools_seperated[1], schools_seperated[2]]
                    
                except:
                    pass
for i in transfer_list:
    playerurl = transfer_list[i][0]
    school = transfer_list[i][2]
    try:
        driver = webdriver.Firefox()
        driver.get(playerurl)
        driver.implicitly_wait(2)
        soup = bs(driver.page_source, 'lxml')
        driver.quit()
        tables = soup.find_all("table")
        table1 = tables[2]
        table2 = tables[4]
        table3 = tables[5]
        table4 = tables[6]
        stats1 = table1.find_all('tr')
        stats2 = table2.find_all('tr')
        stats3 = table3.find_all('tr')
        stats4 = table4.find_all('tr')
        for x in range(len(stats2)):
            if school not in stats2[x].text:
                pass
            else:
                year1 = stats2[x-1].find_all('th')
                year2 = stats2[x].find_all('th')
                transfer_list[i].extend([year1[0].text, year2[0].text]) 
                break
        for x in range(len(stats1)):
            if transfer_list[i][3] in stats1[x].text:
                stats11 = stats1[x].find_all('td')
                for j in range(len(stats11)):
                    transfer_list[i].append(stats11[j].text) 
                break   
            else:
                pass
        for x in range(len(stats2)):
            if transfer_list[i][3] in stats2[x].text:
                stats21 = stats2[x].find_all('td')
                for j in range(len(stats21)):
                    transfer_list[i].append(stats21[j].text) 
                break   
            else:
                pass
        for x in range(len(stats3)):
            if transfer_list[i][3] in stats3[x].text:
                stats31 = stats3[x].find_all('td')
                for j in range(len(stats31)):
                    transfer_list[i].append(stats31[j].text) 
                break   
            else:
                pass
        for x in range(len(stats4)):
            if transfer_list[i][3] in stats4[x].text:
                stats41 = stats4[x].find_all('td')
                for j in range(len(stats41)):
                    transfer_list[i].append(stats41[j].text) 
                break   
            else:
                pass
        for x in range(len(stats1)):
            if transfer_list[i][4] in stats1[x].text:
                stats12 = stats1[x].find_all('td')
                for j in range(len(stats12)):
                    transfer_list[i].append(stats12[j].text) 
                break   
            else:
                pass
        for x in range(len(stats2)):
            if transfer_list[i][4] in stats2[x].text:
                stats22 = stats2[x].find_all('td')
                for j in range(len(stats22)):
                    transfer_list[i].append(stats22[j].text) 
                break   
            else:
                pass
        for x in range(len(stats3)):
            if transfer_list[i][4] in stats3[x].text:
                stats32 = stats3[x].find_all('td')
                for j in range(len(stats32)):
                    transfer_list[i].append(stats32[j].text) 
                break   
            else:
                pass
        for x in range(len(stats4)):
            if transfer_list[i][4] in stats4[x].text:
                stats42 = stats4[x].find_all('td')
                for j in range(len(stats42)):
                    transfer_list[i].append(stats42[j].text) 
                break   
            else:
                pass    
    except:
        print(i)
with open('AllDataOneGo.csv', 'a', newline='') as output:
            writer = csv.writer(output)
            for key, value in transfer_list.items():
                writer.writerow([key, value]) 