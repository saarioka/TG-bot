# -*- coding: utf-8 -*-

import json
import urllib.request
from bs4 import BeautifulSoup
import requests
import datetime
import re


class Reaktori:

    def ruoka(pituus):

        with urllib.request.urlopen("http://www.amica.fi/modules/json/json/Index?costNumber=0812&language=fi") as url:
            data = json.loads(url.read().decode())

        menus = data['MenusForDays'][0]["SetMenus"]
        long = ['Linjasto:']
        short = []

        for i in range(len(menus)):
            for j in range(len(menus[i]["Components"])):
                if menus[i]['Name'] == 'Linjasto':
                    short.append(menus[i]["Components"][j])

        long += short
        long.append('Iltaruoka:')

        for i in range(len(menus)):
            for j in range(len(menus[i]["Components"])):
                if menus[i]['Name'] == 'Iltaruoka':
                    long.append(menus[i]["Components"][j])

        if pituus == 1:
            return "\n".join(short)

        elif pituus == 2:
            return "\n".join(long)

        else:
            print("Error: not found")


class Hertsi:

    def ruoka(pituus):

        r = requests.get("https://www.sodexo.fi/tty-tietotalo")
        data = r.text
        r.close()
        soup = BeautifulSoup(data, "lxml")
        ruuat = soup.find_all('div', attrs={'class': 'lunch_desc inline'})
        apulista = []
        valmis_pitka = []

        for i in range(len(ruuat)):
            apulista.append(ruuat[i].getText().strip().splitlines())

        for j in range(len(apulista)):
            valmis_pitka.append(apulista[j][0])

        valmis_lyhyt = valmis_pitka[0:3]

        if pituus == 1:
            return "\n".join(valmis_lyhyt)

        elif pituus == 2:
            return "\n".join(valmis_pitka)

        else:
            print("Error: not found")


class Juvenes:

    def ruoka(pituus):

        r = requests.get('http://www.juvenes.fi/tabid/338/moduleid/3588/RSS.aspx')
        data = r.text
        r.close()
        soup = BeautifulSoup(data, "lxml")

        date = datetime.date.today().strftime("%d.%m.").lstrip("0").replace("0", "")
        match = None # cannot be initialized in loop
        for item in soup.find_all('item'):
            if date in item.title.text:
                soos = item.description.text
                match = re.findall(r'((?<=<li><strong>)[^<]*)', soos)

        if match:
            return "\n".join(match)

        else:
            print("Error: not found")

            # <li><strong>[^<]+<\/strong>  (?<=<li><strong>)[^<]+(?=<\/strong>)
