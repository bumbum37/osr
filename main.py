#!/data/data/com.termux/files/usr/bin/python
#Source Code
#Bumba
#Refactoring terakhir 29okt,7nov 2021
#5maret2022
from os import path, remove, system;system('clear')
from sys import exit, argv
from bs4 import BeautifulSoup
from colorama import Fore,Style
from random import choice
import requests
import questionary
import re
import tqdm
import os


#Hapus file
if path.exists('links.txt'):
    remove('links.txt')
else:
    open('links.txt', 'x')


#color
color = [
    Fore.BLUE, Fore.CYAN, Fore.GREEN, Fore.LIGHTYELLOW_EX,  Fore.LIGHTRED_EX, Fore.LIGHTGREEN_EX, Fore.LIGHTCYAN_EX, Fore.LIGHTBLUE_EX, Fore.YELLOW
]
def banner(color=choice(color)):
    print(f'''{color}╔═╗╔═╗╦═╗
║ ║╚═╗╠╦╝
╚═╝╚═╝╩╚═
{Style.RESET_ALL}\033[1mOtaku Scrap\n''')


def bypas(url):

    header = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'}
    link = url
    url1 = requests.Session().get(link,headers=header).url

    text = requests.get(link,headers=header).text
    pettern = re.compile(r'\/[\w+.moe.a-zA-Z_-]+--.[a-zA-Z1234567890._p]+\w+')
    name_Anime = pettern.findall(text)

    pettern = re.compile(r'\d{6}\s\%\s\d{5}\s\+\s\d{6}\s\%\s\d{3}')
    match = pettern.findall(text)
    idAnime = (match[0].split(' % '))

    a = 51245
    b = 913
    c = int(idAnime[0])
    id = (c % a + c % b)

    url = re.compile(r'https:\/\/\w+')
    x = (url.findall(url1))
    result = (x[0]+'.zippyshare.com/d/'+str(url1.split('/')[-2])+'/'+str(id)+str(name_Anime[0]))
    return (result)

def mainurl(url):
    session = requests.Session()
    header = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'}
    return BeautifulSoup(requests.Session().get(url,headers=header).text, 'html.parser')

def homepage():
    soup = mainurl('https://otakudesu.watch')
    series = soup.find('div', class_='rseries').find('ul').find_all('li')
    for x in series:
        print(x.find('div',class_='thumbz').text+' | '+x.find('div',class_='epz').text+' => '+x.find('div', class_="epztipe").text)
#requests
banner()
namaAnime = argv[1:]
if namaAnime == []:
    print('''
python main.py <nama anime>

like this:
python main.py danshi koukousei
          ''')
    exit()
namaAnime = namaAnime[0]
soup = mainurl(f'https://otakudesu.watch/?s={namaAnime}&post_type=anime')
uL = soup.find("ul", class_="chivsrc").find_all('li')

if not uL:
    print(Fore.LIGHTRED_EX+'\nMasukan Judul Anime yg benar !\n'+Style.RESET_ALL)
    exit()

#SHOW anme yang masuk ke daftar anime
kuntul = soup.find("ul", class_="chivsrc").find_all('li')
print('\n'+'List Anime'.center(20,'='))
namatext_hasilpwncarian =[] #Nama Teks Anime
hasilpencarian = [] #Link dari Teks Anime
number = 1
for ll in kuntul:
    namatext_hasilpwncarian.append(str(number)+': '+ll.find('h2').find('a').text)
    hasilpencarian.append(ll.find('h2').find('a').get('href'))
    number += 1
#AKHIR show

#AWAL untuk memilih anime
pilihan = questionary.select('Pilih Anime:',choices=namatext_hasilpwncarian,use_shortcuts=(False), use_jk_keys=True, instruction=(' Gunakan panah atau j/k')).ask()
req_link = (hasilpencarian[namatext_hasilpwncarian.index(pilihan)])
print()
scraprequesLink = mainurl(req_link)

sin = scraprequesLink.find('div', class_="fotoanime")
epList = [scraprequesLink.find('div', id="venkonten").find_all('div', class_="episodelist",limit=2)]
#AKHIR untuk memilih anime

#AWAL status anime dan sinopsis
print();system('clear')
for x in sin.find('div',class_='infozingle'):
    print(x.text)
print('\nSinopsis:')
for y in sin.find('div',class_='sinopc'):
    print(y.text.strip())
#AKHIR dari status anime dan sinopsis

#AWAL pisode yang ditampilkan 
listEpisode =[]
name=[]
print('\n'+'Episode List'.center(20,'='))
for e in epList[0]:
    for y in e.find_all('a'):
        name.insert(0,y.text.replace('Subtitle Indonesia',''))
        listEpisode.insert(0,y.get('href'))

for x, y in enumerate(name, start=1):
    print(f'{str(x)}: {y}')
#AKHIR dari episode yang ditampilkan 

#AWAL user memilih episode
eps_kontol = []
pilih_eps_kontol = input('Pilih Eps: ')
if ':' in pilih_eps_kontol:
    pilih_eps_kontol = pilih_eps_kontol.split(':')
    for x in range(int(pilih_eps_kontol[0])-1, int(pilih_eps_kontol[-1])):
        eps_kontol.append(listEpisode[x])
elif pilih_eps_kontol == 'all':
    for x in range(0, len(listEpisode)):
        eps_kontol.append(listEpisode[x])
else:
    eps_kontol.append(listEpisode[int(pilih_eps_kontol)-1])
#AKHIR user memilih episode

#AWAL menampilkan resolusi yang tersedia pada web
print()
scraplink = mainurl(eps_kontol[0])
reps =scraplink.find('div', class_='download').find('ul').find_all('li')
for index,resolusi in enumerate(reps,start=1):
    print(str(index)+': '+resolusi.find('strong').text)
#AKHIR menampilkan resolusi yang tersedia pada web

#AWAL user memilih resolusi dan menampilkan link
n=3
#n = int(input('Pilih resolusi: '))

addText = []
print('\nLink Tersedia:')
with open('links.txt','a') as file:
    for x in eps_kontol:
        scraplink = mainurl(x)
        reps =scraplink.find('div', class_='download').find('ul').find_all('li')

    #jika mau nge Batch pake ini
        haha = ""
        try:
            print(bypas(reps[n-1].find('a').get('href')))
            haha += (bypas(reps[n-1].find('a').get('href'))+'\n')
        except:
            print(reps[n-1].find('a').get('href'))
            haha += (bypas(reps[n-1].find('a').get('href'))+'\n')

        file.write(haha)
exit()
