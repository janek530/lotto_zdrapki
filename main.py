import requests
from bs4 import BeautifulSoup

def usun(text):
    global ilosc_losow
    zmienna_pom = ""
    text_len = len(text)
    for i in range(text_len):
        if text[i] == " ":
            pass
        else:
            zmienna_pom += text[i]
    ilosc_losow = zmienna_pom

def sprawdz(text, slowo):
    global ilosc_losow
    text_len = len(text)
    word_len = len(slowo)
    for i in range(text_len):
        if text[i:i+word_len] == slowo:
            ilosc_losow = text[0:i-1]

def sprawdz_ile(text):
    global sell
    text_len = len(text)
    for i in range(text_len):
        if text[i] == "(":
            sell += int(text[0:i])

def href(text):
    word = "href="
    word2 = "tar"
    len_w = len(word)
    len_w2 = len(word2)
    len_t = len(text)
    pom = 0
    for j in range(0, len_t):
        if text[j:len_w2+j] == word2:
           pom = j
    for x in range(0, len_t):
        if text[x:len_w+x] == word:
            linki.append('https://www.wynikilotto.net.pl'+text[len_w+4:pom-2])

zdrapki = []
szansa = []
linki = []

r = requests.get("https://www.wynikilotto.net.pl/zdrapki/")
soup = BeautifulSoup(r.text, "html.parser")
links_table = soup.find('ul', attrs={'class' : 'tiles'})
links = links_table.find_all('a')
for i in links:
    href(str(i))

for link in linki:
    ilosc_losow = 0
    wygrane = 0
    sell = 0
    line = 0
    sell_win = 0
    prawdopodobienstwo = 0
    sell_p = 0
    sell_all = 0
    print(link)
    r = requests.get(link)
    soup = BeautifulSoup(r.text, "html.parser")

    ilosc = soup.find_all('dd')
    nazwa = soup.find('h1', attrs={'class' : "klasapod"})

    table = soup.find('table', attrs={'class' : 'tabela'})
    wiersz = table.find_all('tr')
    z = 0

    for x in wiersz:
        for i in x:
            if z == 7+line*4:
                wygrane += int(i.text)
            if z == 8+line*4:
                if i.text == "b.d.":
                    sell += 0
                else:
                    sprawdz_ile(i.text)
            z += 1
        if z > 7:
            line += 1

    for x in ilosc:
        sprawdz(str(x.text), 'los')
    sell_win = wygrane - sell
    usun(ilosc_losow)
    prawdopodobienstwo = float(wygrane)/float(ilosc_losow)
    sell_all = float(sell_win)/float(prawdopodobienstwo)
    ilosc_losow = (float(ilosc_losow)-(float(sell_all)))

    zdrapki.append(nazwa.text)
    szansa.append(str(float(sell)/float(ilosc_losow)))
max = max(szansa)
min = min(szansa)
max_z = ""
min_z = ""
result = zip(zdrapki, szansa)
for i, j in result:
    if j == max:
        max_z = i
        print("szansa na wygrana w {} jest rowna: ".format(i) + j + "%")
    elif j == min:
        min_z = i
        print("szansa na wygrana w {} jest rowna: ".format(i) + j + "%")
    else:
        print("szansa na wygrana w {} jest rowna: ".format(i) + j + "%")
print(" \n")
print("#"*120)
print("##  najwieksza szansa na wygraną jest w: " + max_z + " z szansą : "+ max + "%")
print("##  najmniejsza szansa na wygraną jest w: " + min_z + " z szansą : "+ min + "%")
print("#"*120)