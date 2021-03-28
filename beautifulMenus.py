import urllib3
from bs4 import BeautifulSoup
# BeautifulSoup4 documentation: www.crummy.com/software/BeautifulSoup/bs4/doc/
import json
import re
import sys
from datetime import datetime, date, timedelta

import dateparser

restaurants = {
    "Capu": "https://www.crous-bordeaux.fr/restaurant/resto-u-le-capu/", 
    "Mascaret": "https://www.crous-bordeaux.fr/restaurant/resto-u-le-mascaret/", 
    "RU1": "https://www.crous-bordeaux.fr/restaurant/resto-u-n1/", 
    "RU2": "https://www.crous-bordeaux.fr/restaurant/resto-u-n2/",
    "Space Campus": "https://www.crous-bordeaux.fr/restaurant/space-campus-resto-u/", 
    "Veracruz": "https://www.crous-bordeaux.fr/restaurant/crous-cafet-le-veracruz/"
}

covid_messages = [
    r"(Vente (.*?) dessert], )",
    r"(Unique(.*?) :, )",
    r"(, Fruits ou yaourt)",
    r"(Le service (.*?) heures)"
]

empty_messages = [
    "",
    "menu non communiqué",
    "Menu non communiqué",
    "Fermé",
    "fermée",
    "FERMÉ",
    "Pas de service"
]

cafe_titles = [
    "Desserts",
    "CAFETERIA", 
    "Crous Market le Vent debout",
    "Le Crous Market",
    "Le Crous and Go"
]

conditional_titles = [
    "Ventes à emporter",
    "Vente à emporter"
]

def concatenate(strArray):
    res = ', '.join(map(str, strArray))
    return res

def getDate(date):
    date_str = date.string
    date_str = date_str.replace("Menu du ", "")
    
    format_str = '%A %d %B %Y'

    datetime_obj = dateparser.parse(date_str, 
                                    date_formats=[format_str], 
                                    locales=['fr-BE'])

    return str(datetime_obj.date())

def extractDictionary(input):
    res = re.sub(":,", ":", input)
    res = res.split(":")
    if len(res)==1:
        return res[0] 
    if len(res)%2!=0:
        # Split data
        tmp = [res[0]]
        for substr in res[1:-1]:
            tmp += substr.rpartition(',')[::2]
        tmp.append(res[-1])
        res = tmp
    # Create dictionary
    it = iter(res)
    res = dict(zip(it, it))
    return res

def clean(chaine, cnt):
    name = chaine.string
    # Exclude cafe chains
    if name in cafe_titles:
        return None, None
    if name in conditional_titles:
        if cnt>1:
            return None, None
    # Get chain data
    info = chaine.next_sibling
    res = concatenate(info.stripped_strings)
    # Clean information
    for x in covid_messages:
        res = re.sub(x, "", res)
    if res in empty_messages:
        return None, None
    # Extract subdictionaries
    res = extractDictionary(res)
    return name, res

def getMenu(meal):
    menu = meal.string
    if not menu:
        menu = dict()
        chaines = meal.find_all("span", "name")
        cnt = len(chaines)
        pred = None
        for chaine in chaines:
            name, repas = clean(chaine, cnt)
            if name is not None:
                if repas != pred:
                    menu[name] = repas
                    pred = repas
        if len(menu) == 1:
            menu = pred
        if len(menu) == 0:
            menu = "Menu non communiqué"
    return menu

def getToday(dates):
    res = dict()
    allDates = getAll(dates)
    today = str(date.today())
    if today in allDates.keys():
        res[today] = allDates[today]
    else:
        res[today] = {"lunch": "Pas de service", 
                      "dinner": "Pas de service"}
    return res

def getGivenDate(ddmmyy, dates):
    res = dict()
    allDates = getAll(dates)
    day = str(ddmmyy)
    if day in allDates.keys():
        res[day] = allDates[day]
    else:
        res[day] = {"lunch": "Menu non communiqué", 
                      "dinner": "Menu non communiqué"}
    return res   

def getFromDate(date):
    # simplify date structure
    day = getDate(date)
    # get daily meals 
    meals = date.next_sibling.next_sibling
    meals = meals.find_all("div", "content-repas")
    # simplify lunch menu
    lunch = getMenu(meals[1])
    # simplify dinner menu
    dinner = getMenu(meals[2])
    # save menu
    menu = dict()
    menu["lunch"] = lunch
    menu["dinner"] = dinner
    return day, menu

def getAll(dates):
    res = dict()
    for date in dates:
        day, menu = getFromDate(date)
        res[day] = menu
    return res

def getAdvanced(soup, ddmmyy=None):
    # find menu section of page
    menu_repas = soup.find(id="menu-repas")
    # get each date section
    dates = menu_repas.find_all('h3')
    # res = getAll(dates)
    if not ddmmyy:
        res = getToday(dates)
    else:
        res = getGivenDate(ddmmyy, dates)
    return res

def saveAsJSON(filename, lib):
    with open(filename, 'w', encoding='utf8') as json_file:
        json.dump(lib, json_file, indent=4, ensure_ascii=False)

def readJSON(filename):
    f = open(filename, "r", encoding='utf8')
    data = json.load(f) # dictionary
    #keys = data.keys()
    #data = data.items() # tuple list
    menu = data
    print(json.dumps(menu, indent=2, ensure_ascii=False))
    f.close()

def getData(diff = None):
    for res in restaurants.keys():
        # get html data
        url = restaurants[res]
        html = http.request('GET', url).data

        # organise html data
        soup = BeautifulSoup(html, 'html.parser') #, from_encoding="utf-8"
        if not diff:
            menu = getAdvanced(soup)
        else:
            ddmmyy = date.today()+timedelta(days=diff)
            menu = getAdvanced(soup, ddmmyy)

        # save as JSON
        saveAsJSON(res+".json", menu)

def useHTMLData(res):
    # get html data
    f = open(res+".html", "r", encoding='utf8')
    html = f.read()
    f.close()
    # organise html data
    soup = BeautifulSoup(html, 'html.parser') #, from_encoding="utf-8"
    menu = getAdvanced(soup)

    # save as JSON
    saveAsJSON(res+".json", menu) 

def loadAll():
    for res in restaurants.keys():
        print("#####")
        print(res + " - ")
        readJSON(res+".json")
        print("\n")

#input number of days until desired date
diff_date = None
if len(sys.argv)==2:
    diff_date = int(sys.argv[1])

http = urllib3.PoolManager()
getData(diff_date)
# useHTMLData("mascaret")
loadAll()
