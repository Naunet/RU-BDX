import urllib3
import re
import sys

http = None

def clean(item):
    item = item.decode('utf-8')
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
    dinner = clean(res[2])
    return {"lunch" : lunch, "dinner" : dinner}

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
    return {"lunch" : lunch, "dinner" : dinner}

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
    return {"lunch" : lunch, "dinner" : dinner}

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
    return {"lunch" : lunch, "dinner" : dinner}

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
    return {"lunch" : lunch, "dinner" : dinner}

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
    return {"lunch" : lunch, "dinner" : dinner}


def getLunch():
    res = dict()
    
    ###RU1 menu
    lunch, _ = getRU1()
    res["RU1 midi"] = lunch
    
    ###RU2 menu
    lunch, _ = getRU2()
    res["RU2 midi"] = lunch

    ###Veracruz menu
    lunch, _ = getVeracruz()
    res["Veracruz midi"] = lunch

    ###Space Campus menu
    lunch, _ = getSpaceCampus()
    res["Space Campus midi"] = lunch

    ###Mascaret menu
    lunch, _ = getMascaret()
    res["Mascaret midi"] = lunch
    
    ###Capu menu
    lunch, _ = getCapu()
    res["Capu midi"] = lunch
    
    return res

def getDinner():
    res = dict()
    
    ###RU1 menu
    _, dinner = getRU1()
    res["RU1 soir"] = dinner
    
    ###RU2 menu
    _, dinner = getRU2()
    res["RU2 soir"] = dinner

    ###Veracruz menu
    _, dinner = getVeracruz()
    res["Veracruz soir"] = dinner

    ###Space Campus menu
    _, dinner = getSpaceCampus()
    res["Space Campus soir"] = dinner

    ###Mascaret menu
    _, dinner = getMascaret()
    res["Mascaret soir"] = dinner
    
    ###Capu menu
    _, dinner = getCapu()
    res["Capu soir"] = dinner

    return res

def main():
    global http
    http = urllib3.PoolManager()

    res = dict()
    res["Capu"] = getCapu()
    res["Mascaret"] = getMascaret()
    res["RU1"] = getRU1()
    res["RU2"] = getRU2()
    res["Space Campus"] = getSpaceCampus()
    res["Veracruz"] = getVeracruz()
    return res
