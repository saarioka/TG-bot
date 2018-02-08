# -*- coding: utf-8 -*-

import json
import urllib.request
from pprint import pprint
from bs4 import BeautifulSoup
import requests
import lxml

class Reaktori:

    def ruoka(pituus):

        with urllib.request.urlopen("http://www.amica.fi/modules/json/json/Index?costNumber=0812&language=fi") as url:
            data = json.loads(url.read().decode())
        menus = data['MenusForDays'][0]["SetMenus"]
        valmis_pitka = ["Reaktori:"]
        for i in range(len(menus)):
            for j in range(len(menus[i]["Components"])):
                valmis_pitka.append(menus[i]["Components"][j])
        valmis_lyhyt = valmis_pitka
        if pituus == 1:
            return "\n".join(valmis_lyhyt)

        elif pituus == 2:
            return "\n".join(valmis_pitka)
        else:
            print("Error: not found")


class Juvenes:

    def ruoka(pituus):

        with urllib.request.urlopen("http://www.amica.fi/modules/json/json/Index?costNumber=0812&language=fi") as url:
            data = json.loads(url.read().decode())
        menus = data['MenusForDays'][0]["SetMenus"]
        valmis_pitka = ["Reaktori:"]
        for i in range(len(menus)):
            for j in range(len(menus[i]["Components"])):
                valmis_pitka.append(menus[i]["Components"][j])
        valmis_lyhyt = valmis_pitka
        if pituus == 1:
            return "\n".join(valmis_lyhyt)

        elif pituus == 2:
            return "\n".join(valmis_pitka)
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
        valmis_pitka = ["Hertsi:"]

        i=0
        while i in range (len(ruuat)):
            apulista.append(ruuat[i].getText().strip().splitlines())
            i += 1

        j=0
        for j in range(len(apulista)):
            valmis_pitka.append("-" + apulista[j][0])

        valmis_lyhyt = valmis_pitka[0:3]

        if pituus == 1:
            return "\n".join(valmis_lyhyt)

        elif pituus == 2:
            return "\n".join(valmis_pitka)
        else:
            print("Error: not found")