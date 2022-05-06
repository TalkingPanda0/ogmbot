#!/bun/python3
import requests
from bs4 import BeautifulSoup
from json import loads

#def check_duplicate(l):
#    visited = set()
#    for el in l:
#        if el in visited:
#            print(el)
#        else:
#            visited.add(el)

ids = []
def getres(sinifId,dersId,uniteId,kazanimId):
    response = requests.get('https://ogmmateryal.eba.gov.tr/api/soru-secim-listele?sinifId=' + sinifId + '&dersId=' + dersId + '&uniteId=' + uniteId + '&kazanimId=' + kazanimId)
    return response.text

def bsify(html):
    soup = BeautifulSoup(html,features="lxml")
    return soup.get_text()

def getandwrite(sinifId,dersId,uniteId,kazanimId,maxsoru):
    res = getres(sinifId,dersId,uniteId,kazanimId)
    res = loads(res)
    maxsoru -= 1
    with open(uniteId +".txt","a") as f:
        for i in range(maxsoru):
            soru = res[i]
            sid = str(soru['id'])
            if sid in ids:
                continue
            html = f"{i+1}) {soru['baslik']}\nA) {soru['secenekA']}B) {soru['secenekB']}C) {soru['secenekC']}D) {soru['secenekD']}E) {soru['secenekE']}"
            f.write(f"{bsify(html)}\n")
            ids.append(sid)

def getcevaps(ids):
    cevaps = requests.get(f"https://ogmmateryal.eba.gov.tr/soru-bankasi/test-yazdir?id={ids}")
    with open("cevaps.txt","a") as f:
        f.write(cevaps.text)
    return cevaps


cids = ""
for a in range(286,291,1):
    getandwrite("7","56",str(a),"0",101)
print(str(len(ids)+1) + " tane soru buldum.")
for i in ids:
    cids += f"{i},"
getcevaps(cids)

