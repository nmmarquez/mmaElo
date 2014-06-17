# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import requests, os, csv
from lxml import html
import requests, os, csv, io
from lxml import etree as ET
import urllib as url
import re

# <codecell>

### Ininitate Variables
fighters = {'http://en.wikipedia.org/wiki/Nate_Diaz'}
finished = set()
needz = {'http://en.wikipedia.org/wiki/Nate_Diaz'}
n = 0
data = []
one55 = set()
otherDiv = set()

# <codecell>

### build some basic data grabbing functions
def getHTML (URL):
    f = requests.get (URL)
    return (html.fromstring (f.text))

def is155 (htmlTree):
    vcard = htmlTree.xpath ('//table[@class="infobox vcard"]') [0]
    temp2 = ''
    for i in vcard.xpath ('tr'):
        if len (i.xpath ('th')) != 0 and i.xpath ('th') [0].text == 'Division':
            temp2 = i.xpath ('td') [0].text_content()
    return ('Lightweight' in temp2)

def getName (URL):
    return re.sub('_', ' ', re.sub('_\((.*?)\)', '', URL.split ('/') [-1]))

def getFightNum (htmlTree):
    head = htmlTree.xpath ('//span[@id="Mixed_martial_arts_record"]') [0]
    tab = head.getparent().getnext().getnext()
    return len (tab.xpath ('tr')) - 1

def getOppURL (htmlTree):
    opp = set(); base = 'http://en.wikipedia.org'
    head = htmlTree.xpath ('//span[@id="Mixed_martial_arts_record"]') [0]
    tab = head.getparent().getnext().getnext()
    for el in tab.xpath ('tr') [1::]:
        vs = el.xpath ('td') [2]
        try: opp.add (base + vs.xpath ('a') [0].get ('href'))
        except: None
    return (opp)

def getRecord (URL):
    htmlTree = getHTML (URL); name = [getName (URL)]; data = []
    head = htmlTree.xpath ('//span[@id="Mixed_martial_arts_record"]') [0]
    tab = head.getparent().getnext().getnext()
    return [name + [cell.text_content() for cell in el.xpath ('td')]
            for el in tab.xpath ('tr') [1::]]
        

# <codecell>

### Heart of Algorithm
while n < 10000 and len (needz) != 0:
    curr = next(iter(needz))
    needz.remove (curr)
    finished.add (curr)
    hTree = getHTML (curr)
    try:
        if is155 (hTree):
            one55.add (curr)
            if getFightNum (hTree) > 9:
                fighters = fighters.union (getOppURL (hTree))
                data = data + getRecord (curr)
        else:
            otherDiv.add (curr)
    except:
        None
    needz = fighters.difference (finished)
    n += 1
    print (n, curr, len (one55))

# <codecell>

### no more unicode and add headers
data2 = [[d if type (d) == type('str') else d.encode(errors='replace') for d in r]
         for r in data]
data3 = [['fighter', 'outcome', 'record', 'opponent', 'method', 'event', 'date',
          'round', 'time', 'location', 'notes']] + data2

# <codecell>

### need to fix names which means im hard coding which means im failing ugh

rename = {'Andre Pederneiras': ['Andr? Pederneiras', 'Andr%C3%A9 Pederneiras'], 
          "Dom O'grady": ['Dom O%27Grady'], 
          'Fabricio Camoes': ['Fabr?cio Cam?es', 'Fabr%C3%ADcio Cam%C3%B5es'],
          'Fabricio Guerreiro': ['Fabr%C3%ADcio Guerreiro', 'Fabr?cio Guerreiro'], 
          'Hermes Franca': ['Hermes Fran?a', 'Hermes Fran%C3%A7a'],
          'Iuri Alcantara': ['Iuri Alc?ntara', 'Iuri Alc%C3%A2ntara'],
          'Joao Cunha': ['Jo?o Cunha', 'Jo%C3%A3o Cunha'],
          'Jose Aldo': ['Jos%C3%A9 Aldo', 'Jos? Aldo'],
          'Istvan Majoros': ['Istv%C3%A1n Majoros'],
          'Junior Assuncao': ['Junior Assun%C3%A7%C3%A3o', 'Junior Assun??o'],
          'Marcus Aurelio': ['Marcus Aur?lio', 'Marcus Aur%C3%A9lio'],
          'Rene Nazare': ['Ren%C3%AA Nazare', 'Ren? Nazare'],
          'KJ Noons': ['K.J. Noons'],
          'Rocky Johnson': ['Rocky Johnson MMA'],
          'Manvel Gamburyan': ['Manny Gamburyan'],
          'Chan Sung Jung': ['Jung Chan-Sung']
          }

def trans (string):
    change = [i for j in rename.values() for i in j]
    if string in change:
        for k in rename.keys():
            if string in rename [k]:
                return k
    else:
        return string
    
data4 = [[trans (cell) for cell in row] for row in data3]

# <codecell>

#### save the main file
with open("/Users/marqueznm/Google Drive/Elo_Ranking/testing/mma/mma.csv", "wb") as f:
    writer = csv.writer(f)
    writer.writerows(data4)

# <codecell>

### work out who im going to use in the analysis
eligible = list (set([trans(getName (i)) for i in fighters.difference (otherDiv)
            if 'index' not in getName (i) and 'Pancrase' not in getName (i)]))
eligible.sort()
eligibleNamed = ['fighters'] + eligible

one55Names = list (set ([trans (getName (i)) for i in one55]))
one55Names.sort()
one55NamesNamed = ['fighters'] + one55Names

# <codecell>

### save that too
with open("/Users/marqueznm/Google Drive/Elo_Ranking/testing/mma/eligible.csv", 'wb') as f:
    writer = csv.writer(f)
    writer.writerows([[i] for i in eligibleNamed])
    
with open("/Users/marqueznm/Google Drive/Elo_Ranking/testing/mma/one55.csv", 'wb') as f:
    writer = csv.writer(f)
    writer.writerows([[i] for i in one55NamesNamed])

