#!/usr/bin/env python3
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import html5lib
import pdb
import json
import csv
from collections import OrderedDict

wiki = "http://www.espn.com/mens-college-basketball/tournament/bracket"
page = urlopen(wiki)
soup = BeautifulSoup(page, "html5lib")

region = soup.findAll("div", {"class": "regtitle"})
R=[]
for row in region:
    R.append(row.find(text=True))
#pdb.set_trace()

venue1 = soup.findAll("div", {"class": "venue v1"})
V1=[]
for row in venue1:
    V1.append(row.find(text=True))
venue2 = soup.findAll("div", {"class": "venue v2"})
V2=[]
for row in venue2:
    V2.append(row.find(text=True))
venue3 = soup.findAll("div", {"class": "venue v3"})
V3=[]
for row in venue3:
    V3.append(row.find(text=True))
venue4 = soup.findAll("div", {"class": "venue v4"})
V4=[]
for row in venue4:
    V4.append(row.find(text=True))
venue5 = soup.findAll("div", {"class": "venue v5"})
V5=[]
for row in venue5:
    V5.append(row.find(text=True))
venuef = soup.findAll("div", {"class": "venue final"})
VF=[]
for row in venuef:
    VF.append(row.find(text=True))
#pdb.set_trace()

IDX=[]
A=[]
B=[]
C=[]
D=[]
E=[]
F=[]
RX=[]
VX=[]
RO=[]
index = 0
for row in soup.findAll("dl"):
    index+=1
    info=row.findAll(text=True)
    #pdb.set_trace()
    IDX.append(index)
    A.append(info[0])
    B.append(info[1])
    C.append(info[4])
    D.append(info[2])
    E.append(info[3])
    F.append(info[5])
    if (index == 1):
        RX.append(R[3]) #South
        RO.append(0)
    elif (index in range(2, 4)):
        RX.append(R[0]) #East
        RO.append(0)
    elif (index == 4):
        RX.append(R[2]) #Midwest
        RO.append(0)
    elif (index in range(5, 13)):
        RX.append(R[0]) #East
        RO.append(1)
    elif (index in range(13, 17)):
        RX.append(R[0]) #East
        RO.append(2)
    elif (index in range(17, 19)):
        RX.append(R[0]) #East
        RO.append(3)
    elif (index == 19):
        RX.append(R[0]) #East
        RO.append(4)
    elif (index in range(20, 28)):
        RX.append(R[1]) #West
        RO.append(1)
    elif (index in range(28, 32)):
        RX.append(R[1]) #West
        RO.append(2)
    elif (index in range(32, 34)):
        RX.append(R[1]) #West
        RO.append(3)
    elif (index == 34):
        RX.append(R[1]) #West
        RO.append(4)
    elif (index in range(35, 43)):
        RX.append(R[2]) #Midwest
        RO.append(1)
    elif (index in range(43, 47)):
        RX.append(R[2]) #Midwest
        RO.append(2)
    elif (index in range(47, 49)):
        RX.append(R[2]) #Midwest
        RO.append(3)
    elif (index == 49):
        RX.append(R[2]) #Midwest
        RO.append(4)
    elif (index in range(50, 58)):
        RX.append(R[3]) #South
        RO.append(1)
    elif (index in range(58, 62)):
        RX.append(R[3]) #South
        RO.append(2)
    elif (index in range(62, 64)):
        RX.append(R[3]) #South
        RO.append(3)
    elif (index == 64):
        RX.append(R[3]) #South
        RO.append(4)
    elif (index in range(65, 67)):
        RX.append("Final Four")
        RO.append(5)
    elif (index == 67):
        RX.append("Championship") 
        RO.append(6)
    else :
        RX.append("?")
        RO.append("?")
    if (index in range(5, 7) or index == 13):
        VX.append(V1[0])
    elif (index in range(20, 22) or index == 28):
        VX.append(V1[1])
    elif (index in range(35, 37) or index == 43):
        VX.append(V1[2])
    elif (index in range(50, 52) or index == 58):
        VX.append(V1[3])
    else:
        VX.append("?")

df=pd.DataFrame(IDX, columns=['Index'])
df['SeedA']=A
df['TeamA']=B
df['ScoreA']=C
df['SeedB']=D
df['TeamB']=E
df['ScoreB']=F
df['Region']=RX
df['Venue']=VX
df['Round']=RO

with open('espn.json', 'w') as f:
    f.write(df.to_json(orient='index'))

with open("espn.json") as espn_json:
    dict_espn = json.load(espn_json, object_pairs_hook=OrderedDict)
espn_sheet = open('espn.csv', 'w')
csvwriter = csv.writer(espn_sheet)
count = 0
for row in dict_espn.values():
    #pdb.set_trace()
    if (count == 0):
        header = row.keys()
        csvwriter.writerow(header)
        count += 1
    csvwriter.writerow(row.values())
espn_sheet.close()

