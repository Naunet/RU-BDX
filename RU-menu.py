import urllib3
import requests, json
import re
import sys

def clean(item):
    item = item.decode('utf-8') #ansi
    item = item.replace('<li>', '')
    item = item.replace('</li>', ' ')
    item = item.replace('\t', ' ')
    return item

def getRU1():
    #variables
    url = "https://www.crous-bordeaux.fr/restaurant/resto-u-n1/"
    pattern = b'(?<=Plat chaud :)(.+?)(?=</ul>)'
    #get data
    html = http.request('GET', url).data
    #process data
    res = re.findall(pattern, html)
    if not res:
        raise AttributeError("HTML has been updated, desired data not found")
    lunch = clean(res[0])
    dinner = clean(res[1])
    return lunch, dinner

def getRU2():
    #variables
    url = "https://www.crous-bordeaux.fr/restaurant/resto-u-n2/"
    pattern = b'(?<=Uniquement en vente)(.+? :)(.+?)(?=<\/ul>)'
    #get data
    html = http.request('GET', url).data
    #process data
    res = re.findall(pattern, html)
    if not res:
        raise AttributeError("HTML has been updated, desired data not found")
    lunch = clean(res[0][1])
    dinner = clean(res[1][1])
    return lunch, dinner

def getVeracruz():
    #variables
    url = "https://www.crous-bordeaux.fr/restaurant/crous-cafet-le-veracruz/"
    pattern = b'(?<=<div class="content-repas"><div><span class="name">)(.+?)(?=</span>)'
    #get data
    html = http.request('GET', url).data
    #process data
    res = re.findall(pattern, html)
    if not res:
        raise AttributeError("HTML has been updated, desired data not found")
    lunch = clean(res[1])
    dinner = clean(res[2])
    return lunch, dinner

def getSpaceCampus():
    #variables
    url = "https://www.crous-bordeaux.fr/restaurant/space-campus-resto-u/"
    pattern = b'(?<=Grill</span><ul class="liste-plats">)(.+?)(?=</ul>)'
    #get data
    html = http.request('GET', url).data
    #process data
    res = re.findall(pattern, html)
    if not res:
        raise AttributeError("HTML has been updated, desired data not found")
    lunch = clean(res[0])
    dinner = clean(res[1])
    return lunch, dinner

def getMascaret():
    #variables
    url = "https://www.crous-bordeaux.fr/restaurant/resto-u-le-mascaret/"
    pattern = b'(?<=<ul class="liste-plats">)(.+?)(?=<\/ul>)'
    #get data
    html = http.request('GET', url).data
    #process data
    res = re.findall(pattern, html)
    if not res:
        raise AttributeError("HTML has been updated, desired data not found")
    lunch = clean(res[0])
    dinner = clean(res[1])
    return lunch, dinner

def getCapu():
    #variables
    url = "https://www.crous-bordeaux.fr/restaurant/resto-u-le-capu/"
    pattern = b'(?<=Menu</span><ul class="liste-plats">)(.+?)(?=<\/ul>)'
    #get data
    html = http.request('GET', url).data
    #process data
    res = re.findall(pattern, html)
    if not res:
        raise AttributeError("HTML has been updated, desired data not found")
    lunch = clean(res[0])
    dinner = clean(res[1])
    return lunch, dinner

# Initialise
http = urllib3.PoolManager()

#input 0 for lunch and 1 for dinner
isLunch = 1
if len(sys.argv)==2:
    isLunch = 1-int(sys.argv[1])

if isLunch:
	###RU1 menu
	lunch, _ = getRU1()
	print("RU1 midi : " + lunch)

	###RU2 menu
	lunch, _ = getRU2()
	print("RU2 midi : " + lunch)

	###Veracruz menu
	lunch, _ = getVeracruz()
	print("Veracruz midi : " + lunch)

	###Space Campus menu
	lunch, _ = getSpaceCampus()
	print("Space Campus midi : " + lunch)

	###Mascaret menu
	lunch, _ = getMascaret()
	print("Mascaret midi : " + lunch)

	###Capu menu
	lunch, _ = getCapu()
	print("Capu midi : " + lunch)

else: #dinner
	###RU1 menu
	_, dinner = getRU1()
	print("RU1 soir : " + dinner)

	###RU2 menu
	_, dinner = getRU2()
	print("RU2 soir : " + dinner)

	###Veracruz menu
	_, dinner = getVeracruz()
	print("Veracruz soir : " + dinner)

	###Space Campus menu
	_, dinner = getSpaceCampus()
	print("Space Campus soir : " + dinner)

	###Mascaret menu
	_, dinner = getMascaret()
	print("Mascaret soir : " + dinner)

	###Capu menu
	_, dinner = getCapu()
	print("Capu soir : " + dinner)

