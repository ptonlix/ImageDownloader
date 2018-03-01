from os import chdir
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
from urllib.parse import urlencode
from os import walk
import json
from os.path import curdir
from urllib.request import urlretrieve
from os.path import pardir
from create_dir import create_directory
import re
BAIDU_IMAGE = 'http://image.baidu.com/search/index?tn=baiduimage&ps=1&ct=201326592&lm=-1&cl=2&nc=1&ie=utf-8&'
WALLPAPERS_KRAFT = 'https://wallpaperscraft.com/search/keywords?'
usr_agent = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'
        }

def image_grabber(ch):
    if ch==1:
        print('Enter data to download images: ')
        data = input()
        search_query = {'word' : data}
        search = urlencode(search_query)
        print(search)
        g = BAIDU_IMAGE+search
        request = Request(g, headers=usr_agent)
        r = urlopen(request).read()
        print(type(r))
        sew = bytes.decode(r)
        pic_url = re.findall('"objURL":"(.*?)",', sew, re.S)
        print(pic_url)
        counter = 1
        for each in pic_url:
            print('Downloading images ' + str(counter) + ' picture:' + str(each))
            try:
                pic = requests.get(each, timeout=10)
            except requests.exceptions.ConnectionError:
                print('【error】The current image cannot be downloaded.')
                continue
            with open('img' + str(counter) + '.jpg', 'wb') as file:
                file.write(pic.content)
                counter += 1
        return True
    elif ch == 2:
        cont = set()
        temp = set()

        print('Enter data to download wallpapers: ')
        data = input()
        search_query = {'q':data}
        search = urlencode(search_query)
        print(search)

        g = WALLPAPERS_KRAFT+search
        request = Request(g, headers=usr_agent)
        r = urlopen(request).read()
        sew = BeautifulSoup(r, 'html.parser')
        counter = 0
        for links in sew.find_all('a'):
            if 'wallpaperscraft.com/download' in links.get('href'):
                cont.add(links.get('href'))
        for retemp in cont:
            temp.add('https://wallpaperscraft.com/image/' + retemp[31:-10] + '_' + retemp[-9:] + '.jpg')
        for retemp in temp:
            print('Downloading images ' + str(counter) + ' picture:' + str(retemp))
            try:
                pic = requests.get(retemp, timeout=10)
            except requests.exceptions.ConnectionError:
                print('【error】The current image cannot be downloaded.')
                continue
            with open('img' + str(counter) + '.jpg', 'wb') as file:
                file.write(pic.content)
                counter += 1
        return True
    elif ch == 3:
        for folders, subfolder, files in walk(curdir):
            for folder in subfolder:
                print(folder)
        return True
    elif ch == 4:
        print('Enter the directory to be set: ')
        data = input()
        chdir(data + ':\\')
        print('Enter name for the folder: ')
        data = input()
        create_directory(data)
        return True

    elif ch == 5:
        print(
            '''
     -------------------------***Thank You For Using***-------------------------
            '''
        )
        return False
run = True

print(
        '''
***********[First Creating Folder To Save Your Images}***********
    '''
    )
create_directory('Images')
DEFAULT_DIRECTORY = pardir + '\\Images'
chdir(DEFAULT_DIRECTORY)

while run:
    print('''
    -------------------------WELCOME-------------------------
        1. Search for Baidu image
        2. Download Wallpapers 1080p
        3. View Images in your directory
        4. Set directory
        5. Exit
    -------------------------*******-------------------------
        ''')
    choice = input()
    run = image_grabber(int(choice))
