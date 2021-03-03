import json
import scraper

def saveAsJSON(filename, lib):
    f = open(filename, "w")
    f.write(json.dumps(lib, sort_keys=True, indent=4))
    f.close()

def readJSON(filename):
    f = open(filename, "r")
    data = json.load(f) #dictionary
    # Checking content
    mandatory_keys = ['lunch', 'dinner']

    for key in mandatory_keys:
        if key not in data:
            raise ValueError("Cannot find '" + key + "'")
    
    lunch = data['lunch']
    dinner = data['dinner']
    print("\tMidi : " + lunch + ",\n\tSoir : " + dinner)

def updateMenus():
    res = scraper.main()
    for restaurant in res.keys():
        saveAsJSON(restaurant+".json", res[restaurant])

def loadMenu(restaurant):
    print(restaurant + " - ")
    readJSON(restaurant+".json")

def loadAll():
    restaurants = ["Capu", "Mascaret", "RU1", "RU2", "Space Campus", "Veracruz"]
    for restaurant in restaurants:
        loadMenu(restaurant)

updateMenus()
loadAll()