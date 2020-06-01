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


component = namedtuple('component', 'Comment, Description, Designator, Kolicina, PartNo,Datasheet,cena,link')


def parse_ride(line: str) -> component :
    """Parse a line from a Strava log file into a `Ride`. Line format is tab separated:
    Ride	Thu, 8/9/2018	BRNW	4:58:07	68.41 mi	3,862 ft"""
    comment, Description, Designator, Kolicina, PartNo,Datasheet,a1,a2= line.strip().split('\t')
    print(line.strip().split('\t'))
    
    return component(comment,Description, Designator, Kolicina,PartNo,Datasheet,a1,a2)

def number(string) -> float: return float(re.sub(r'[^0-9. ]', '', string))

def hours(sec, min, hour=0) -> float: return int(sec)/3600 + int(min)/60 + int(hour)

components = [parse_ride(line) for line in open('BOMprototip2.tsv') 
         if line.strip() and not "Cena" in line and "buck mosfet" not in line and 'Headeri' not in line and '	0 ft' not in line]

buckMos=component("Ulazni buck mosfet","","Q?",	"4",	"TPN2R903PL,L1Q","","","https://www.digikey.com/product-detail/en/toshiba-semiconductor-and-storage/TPN2R903PLL1Q/264-TPN2R903PLL1QCT-ND/10447157") #ovo izaziva bagove popraviti
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
    #a=("https://www.digikey.com/products/en?keywords="+component.PartNo)
    a=component.link
    driver.get(a)
    """
    if "\n\nPrice Break" not in getPageSource():
         odrediDrugu()
         print("nema")
         "Ovde je potrebno izvuci iz koda sajta digi key part number i promeniti link koji se posecuje na tu adresu, i odatle ponovo pristupiti ceni."
         stranice.append(getPageSource())
    else:    
    """    
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
def SrediX(x):
    if len(x)>1000:
        x=x.split("\nImport Tariff")[0]
    return x  
    
cenice=[]    
for s in stranice:    
        cenice.append(getPrice())
        
ceniceNove=[SrediX(x) for x in cenice]   
ceniceNoveNove=[c.strip(" ").split("\n") for c in ceniceNove]
ceniceNoveNove=[c[2:] for c in ceniceNoveNove]     
        
def Matrici(golub):        
    return [g.split("|") for g in golub]

ceniceNoveNove=[Matrici(c) for c in ceniceNoveNove]

def MakniZadnji(lele):
    if  len(lele[-1])<3:
        lele.pop()
    return lele
ceniceNoveNove=[MakniZadnji(c) for c in ceniceNoveNove]
def Maknipreko(lele,n=1000):  
    for i in range (len(lele)-1): 
        if "," in lele[i][0]:
            lele[i][0]=lele[i][0].replace(",","")
        if int(lele[i][0])>n:
          lele.pop()
    return  lele      
    
ceniceNoveNove=[Maknipreko(c) for c in ceniceNoveNove]        

#Potrebno je provaliti najnizu cenu kada se uzme najveci broj komponenata
#min(ceniceNoveNove[1][i][0] for i in range(len(ceniceNoveNove[1])))      

#Ovo prebaciti u neku funkciju
ceniceNoveNove=[ceniceNoveNove[i][len(ceniceNoveNove[i])-1][1] for i in range(len(ceniceNoveNove))] 

#Mora se pomnoziti pravi indeks sa pravom komponentom i nesto da se pomnozi
#cenaTotal=sum([float(c) for c in ceniceNoveNove])
# BabaMangup[3]*int(components[3].Kolicina) ovo radi
BabaMangup=[float(c) for c in ceniceNoveNove]
cenaTotal=0
for i in range(len(ceniceNoveNove)):
    print("Cena za nejveci moguci broj komada na digikey:" +str(BabaMangup[i])+"\n")
    print("Broj komada na PCB-u"+str(components[i].Kolicina)+"\n")
    cenaTotal+=BabaMangup[i]*int(components[i].Kolicina)
cenaTotal+=0.05651*15
cenaTotal+=12
#nisu dobro sortirane sve komponente i cene izdebagovati    
#cenaTotal  je bila poslednji put 78 dolara jos 12 za pcb i jos 4 za neuracunat dupli kondenzator, ostaje da se izdebaguje dalje ova skripta  
"""
[['1 ', '  0.34000 ', ' $0.34  '],
 ['10 ', ' 0.28600 ', ' $2.86  '],
 ['100 ', ' 0.11160 ', ' $11.16  '],
 ['1,000 ', ' 0.04673 ', ' $46.73  '],
 ['2,500 ', ' 0.04284 ', ' $107.09']]

"""
