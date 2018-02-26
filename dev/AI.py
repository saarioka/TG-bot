# -*- coding: utf-8 -*-

from chatterbot.trainers import ListTrainer
from chatterbot import ChatBot

import re


def alusta_tiedosto():

    tiedosto1 = open("lit.txt", "r", encoding="utf8")
    tiedosto2 = open("lit2.txt", "w", encoding="utf8")

    for rivi in tiedosto1:

        matchObj = re.match(r'(.*), (.*) - (.*): (.*)\n', rivi)

        if matchObj:
            teksti = matchObj.group(4)
            if "<Media jätetty pois>" not in teksti and "https" not in teksti and len(teksti) < 40:
                tiedosto2.writelines(teksti.lower() + "\n")


alusta_tiedosto()
bot = ChatBot("Shaq")
keskustelu = open("lit2.txt", "r", encoding="utf8").readlines()
bot.set_trainer(ListTrainer)
#bot.train(keskustelu)

while True:
    request = input("Santeri: ")
    response = bot.get_response(request)

    print("Shaq: ", response)