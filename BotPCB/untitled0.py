#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 30 15:59:59 2020
Cena prototipa na osnovu BOM-a.
Ulaz programa je excel tabela sa Comment	Description	Designator	Kolicina na ploci	Manufacturer Part Number	Datasheet
A izlaz programa je excel tabela sa Comment	Description	Designator	Kolicina na ploci	Manufacturer Part Number	Datasheet	Cena [USD] i na kraju total cenom.
	
@author: marko
"""


import matplotlib.pyplot as plt
import numpy as np
import re
from collections import namedtuple
from selenium import webdriver
import urllib.request
from webdriver_manager.chrome import ChromeDriverManager
import html2text
h = html2text.HTML2Text()
h.ignore_links = True

def getPageSource():
    return h.handle(str(driver.page_source))


component = namedtuple('component', 'Comment, Description, Designator, Kolicina, PartNo,Datasheet')


def parse_ride(line: str) -> component :
    """Parse a line from a Strava log file into a `Ride`. Line format is tab separated:
    Ride	Thu, 8/9/2018	BRNW	4:58:07	68.41 mi	3,862 ft"""
    comment, Description, Designator, Kolicina, PartNo,Datasheet= line.strip().split('\t')
    #print(line.strip().split('\t'))
    
    return component(comment,Description, Designator, Kolicina,PartNo,Datasheet)

def number(string) -> float: return float(re.sub(r'[^0-9. ]', '', string))

def hours(sec, min, hour=0) -> float: return int(sec)/3600 + int(min)/60 + int(hour)

components = [parse_ride(line) for line in open('BOMprototip2.tsv') 
         if line.strip() and not "Cena" in line and "buck mosfet" not in line and 'Headeri' not in line and '	0 ft' not in line]

buckMos=component("Ulazni buck mosfet","","Q?",	"4",	"TPN2R903PL,L1Q","")
components.append(buckMos)
def getText():
    "Dohvati tekst iz ucitane internet stranice"
    return 1
def odrediDrugu():
    "Odredi drugu stranicu gde mogu naci podatke o ceni"
    return 1
driver =webdriver.Chrome(ChromeDriverManager().install())
stranice=[]
for component in components:
    a=("https://www.digikey.com/products/en?keywords="+component.PartNo)
    driver.get(a)
    if "\n\nPrice Break" not in getPageSource():
         odrediDrugu()
         print("nema")
         "Ovde je potrebno izvuci iz koda sajta digi key part number i promeniti link koji se posecuje na tu adresu, i odatle ponovo pristupiti ceni."
         stranice.append(getPageSource())
    else:    
        stranice.append(getPageSource())
#[Descending](//www.digikey.com/-/media/images/global/icons/dnblack.gif)
# "["str(str(component.PartNo))+"\nDatasheet]"  
#        CL05A105JQ5NNNC
        
def getNextLink(stranica):
        a=stranica.split("Minimum:")
        minimi=[]
        for i in range(len(a)-1):
            minimi.append(a[i+1].split("|")[0])    
        #potrebno je iz stranice iseci 6 "|" ulevo kada se uradi split na minimum:    
        return minimi

def getPrice():
    b=s.split("\n\nPrice Break")
    if len(b)>1:
        c=b[1].split("\n  \nSubmit")
        return c[0]
    else:
        return ""    
cenice=[]    
for s in stranice:    
        cenice.append(getPrice())
        
        
      

