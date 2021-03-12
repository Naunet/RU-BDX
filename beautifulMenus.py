import urllib3
from bs4 import BeautifulSoup
# BeautifulSoup4 documentation: www.crummy.com/software/BeautifulSoup/bs4/doc/
import json

restaurants = {
    "Capu": "https://www.crous-bordeaux.fr/restaurant/resto-u-le-capu/", 
    "Mascaret": "https://www.crous-bordeaux.fr/restaurant/resto-u-le-mascaret/", 
    "RU1": "https://www.crous-bordeaux.fr/restaurant/resto-u-n1/", 
    "RU2": "https://www.crous-bordeaux.fr/restaurant/resto-u-n2/",
    "Space Campus": "https://www.crous-bordeaux.fr/restaurant/space-campus-resto-u/", 
    "Veracruz": "https://www.crous-bordeaux.fr/restaurant/crous-cafet-le-veracruz/"
}

def concatenate(strArray):
    res = ', '.join(map(str, strArray))
    return res

def getDate(date):
    res = date.string
    res = res.replace("Menu du ", "")
    return res

def getMenu(meal):
    menu = meal.string
    if not menu:
        menu = dict()
        chaines = meal.find_all("span", "name")
        for chaine in chaines:
            name = chaine.string
            info = chaine.next_sibling
            menu[name] = concatenate(info.stripped_strings)
    return menu

def getFirst(dates):
    res = dict()
    date = dates[0]
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
    res[day] = menu
    return res

def getAll(dates):
    res = dict()
    for date in dates:
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
        res[day] = menu
    return res

def getAdvanced(soup):
    # find menu section of page
    menu_repas = soup.find(id="menu-repas")
    # get each date section
    dates = menu_repas.find_all('h3')
    #res = getAll(dates)
    res = getFirst(dates)
    return res

def saveAsJSON(filename, lib):
    f = open(filename, "w")
    f.write(json.dumps(lib, indent=4))
    f.close()

def readJSON(filename):
    f = open(filename, "r")
    data = json.load(f) #dictionary
    keys = data.keys()
    menu = data
    print(json.dumps(menu, indent=2))

def loadAll():
    for res in restaurants.keys():
        print("#####")
        print(res + " - ")
        readJSON(res+".json")
        print("\n")

http = urllib3.PoolManager()

for res in restaurants.keys():
    # get html data
    url = restaurants[res]
    html = http.request('GET', url).data

    # organise html data
    soup = BeautifulSoup(html, 'html.parser') #, from_encoding="utf-8"
    menu = getAdvanced(soup)

    # save as JSON
    saveAsJSON(res+".json", menu)

loadAll()