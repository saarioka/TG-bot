# -*- coding: utf-8 -*-

import time
import random
import datetime

# telepot
import telepot
import telepot.helper
from telepot.loop import MessageLoop
from telepot.namedtuple import (
    InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove)
from telepot.delegate import (
    per_chat_id, create_open, pave_event_space, include_callback_query_chat_id)

# ruoka
from Ruokalistat import Reaktori, Hertsi

# chatterbot
from chatterbot.trainers import ListTrainer
from chatterbot import ChatBot
import re


class Shaq(telepot.helper.ChatHandler):

    def __init__(self, *args, **kwargs):
        super(Shaq, self).__init__(*args, **kwargs)

        with open('C:/Users/Santeri/Documents/Python/TG-bot/release/lyrics.txt') as f:
            self._lyrics = f.readlines()
        self._lyrics = [x.strip() for x in self._lyrics]
        self._startup_time = time.time()

        self.bumper = ''
        self.msglist = []
        self.keyboard = ReplyKeyboardRemove()

        #chatter
        #self.prep_learn_file()
        self.chatter = ChatBot("Shaq")
        conv = open("lit2.txt", "r", encoding="utf8").readlines()
        self.chatter.set_trainer(ListTrainer)
        #self.chatter.train(conv)

        # self.sender.sendMessage("Shaq is in the house, boys!")

    def print_time_in(self, msg):
        apu = ''
        if msg['chat']['id'] < 0:
            apu = msg['chat']['title'] + '|'
        print('[' + datetime.datetime.fromtimestamp(msg['date']).strftime('%H:%M:%S') + '] in  ' + apu + msg['from'][
            'first_name'] + ":", end=" ")

    def print_time_out(self, msg):
        apu = ''
        if msg['chat']['id'] < 0:
            apu = msg['chat']['title'] + '|'
        print('[' + datetime.datetime.fromtimestamp(msg['date']).strftime('%H:%M:%S') + '] out ' + apu + msg['from'][
            'first_name'] + ":", end=" ")

    def prep_learn_file(self):

        file1 = open("lit.txt", "r", encoding="utf8")
        file2 = open("lit2.txt", "w", encoding="utf8")

        for line in file1:

            match = re.match(r'(.*), (.*) - (.*): (.*)\n', line)

            if match:
                text = match.group(4)
                if "<Media jätetty pois>" not in text and "https" not in text and len(text) < 40:
                    file2.writelines(text.lower() + "\n")


    #TODO
    def admin(self, msg):
        print("admin in the house")

    def lyrics(self, msg):
        if msg['text'].lower() == '/lyrics':
            self.sender.sendMessage("\n".join(self._lyrics))
            self.print_time_out(msg)
            print('/lyrics')

    def kiitos(self, msg):
        self.sender.sendMessage('Kiitos')
        self.print_time_out(msg)
        print('kiitos')

    def greetings(self, msg):
        greetings_out = ['Helo', 'heyhey', 'Yooyoo', 'Hello', 'Hi', 'Heyyy', 'Hei', 'Hey', 'Moi', 'Moi', 'Moikka',
                         'Helou', 'What\'s up big man']
        self.sender.sendMessage(random.choice(greetings_out) + ' ' + msg['from']['first_name'])
        self.print_time_out(msg)
        print('greetings')

    def pilasib(self, msg):
        lyrics_match = []
        for i in range(len(self._lyrics)):
            if msg['text'].lower() in self._lyrics[i].lower() and len(msg['text']) > 3:
                lyrics_match.append(self._lyrics[i])
        if len(lyrics_match) > 0:
            rand = random.randint(0, len(lyrics_match))
            try:
                self.sender.sendMessage(lyrics_match[rand] + '\n' + lyrics_match[rand + 1])
                self.print_time_out(msg)
            except IndexError:
                try:
                    self.sender.sendMessage(lyrics_match[rand - 1] + '\n' + lyrics_match[rand])
                    self.print_time_out(msg)
                    print(len(lyrics_match))
                except IndexError:
                    self.sender.sendMessage(random.choice(lyrics_match))
            print('lyrics (matches: ' + str(len(lyrics_match)) + ')')

    def Vitsi(self):

        with open('C:/Users/Santeri/Documents/TelegramBot/jokes.txt') as f:
            line = f.readlines()
        jokes_final = []
        apulista = []

        for i in range(len(line)):
            if len(line[i]) > 1:
                apulista.append(line[i])
            else:
                jokes_final.append("".join(apulista))
                apulista.clear()

        self.sender.sendMessage(random.choice(jokes_final))

    def kysely(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)

        self.keyboard = InlineKeyboardMarkup(inline_keyboard=[[
            InlineKeyboardButton(text='Hertsi', callback_data='/hertsi'),
            InlineKeyboardButton(text='Reaktori', callback_data='/reaktori'),
        ], [InlineKeyboardButton(text='<<<', callback_data='/cancel'),
            InlineKeyboardButton(text='Vitsi', callback_data='/vitsi')]])

        bot.sendMessage(chat_id, 'Mitä laitetaan?', reply_markup=self.keyboard)

    def on_callback_query(self, msg):
        query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')

        if query_data == '/hertsi':
            self.sender.sendMessage(Hertsi.ruoka(1))

        if query_data == '/reaktori':
            self.sender.sendMessage(Reaktori.ruoka(1))

        #if query_data == '/cancel':
            #TODO
            #self.bot.editMessageReplyMarkup(msg['message_id'], reply_markup=False, )

        if query_data == '/vitsi':
            print("Ei.")

        self.bot.answerCallbackQuery(query_id)

    # "main"
    def on_chat_message(self, msg):
        try:
            greetings_in = ['moi', 'hei shaq', 'yo', 'yoyo', 'helou', "moi shaq", "hei", "moikka", "moikka shaq"]

            # old message, don't answer
            if msg['date'] < self._startup_time - 10:
                self.print_time_in(msg)
                print(msg['text'])

            else:
                if msg["from"]["id"] == 340000985 and msg['text'].lower().find('sudo') == 0:
                    self.admin(msg)

                # Prints message to shell
                self.print_time_in(msg)
                print(msg['text'])

                # Adds message to list if there is no combo on other chat
                if len(self.msglist) > 1:
                    if (not (self.msglist[-2]['text'].lower() == self.msglist[-1]['text'].lower()
                             and self.msglist[-2]['chat']['id'] == self.msglist[-1]['chat']['id']
                             and msg['chat']['id'] != self.msglist[-1]['chat']['id'])):
                        self.msglist.append(msg)
                else:
                    self.msglist.append(msg)

                # pilasib
                if (len(self.msglist) > 2
                        and self.msglist[-3]['text'].lower() == self.msglist[-2]['text'].lower()
                        and self.msglist[-2]['text'].lower() != self.msglist[-1]['text'].lower()
                        and self.msglist[-3]['chat']['id'] == self.msglist[-2]['chat']['id']
                        and self.msglist[-2]['chat']['id'] == self.msglist[-1]['chat']['id']):
                    self.sender.sendMessage('pilasib')
                    self.print_time_out(msg)
                    print('pilasib')

                # lyrics
                elif msg['text'].lower() == '/lyrics':
                    self.lyrics(msg)

                # greetings
                elif msg['text'].lower() in greetings_in:
                    self.greetings(msg)

                # kiitos
                elif msg['text'].lower().find('kiitos') == 0:
                    self.kiitos(msg)

                # Command:hertsi1
                elif msg['text'].lower().find('/hertsi') == 0:
                    self.sender.sendMessage(Hertsi.ruoka(1))
                    self.print_time_out(msg)
                    print('hertsi1')

                # Command:hertsi2
                elif msg['text'].lower().find('/hertsi2') == 0:
                    self.sender.sendMessage(Hertsi.ruoka(2))
                    self.print_time_out(msg)
                    print('hertsi2')

                # Command:Reaktori1
                elif msg['text'].lower().find('/reaktori') == 0:
                    self.sender.sendMessage(Reaktori.ruoka(1))
                    self.print_time_out(msg)
                    print('reaktori1')

                # Command:Reaktori2
                elif msg['text'].lower().find('/reaktori2') == 0:
                    self.sender.sendMessage(Reaktori.ruoka(2))
                    self.print_time_out(msg)
                    print('reaktori2')

                # kysely
                elif msg['text'].lower().find('/kysely') == 0:
                    self.kysely(msg)

                else:
                    self.bumper += msg['text'] + '\n'

                    if msg['date'] > time.time() - 5:
                        if len(self.bumper) > 0:
                            self.bumper = self.bumper[:-1]

                        print(self.bumper)
                        request = self.bumper.lower()
                        response = self.chatter.get_response(request)

                        self.sender.sendMessage(str(response))
                        self.print_time_out(msg)
                        print(response)
                        self.bumper = ''

                # Command:lyrics
                self.pilasib(msg)

                # Deletes old message(s) from list
                if len(self.msglist) > 1 and self.msglist[-1]['text'].lower() != self.msglist[-2]['text'].lower():
                    del self.msglist[0:-2]

        except KeyError:
            print('Sticker/Picture/Other')


TOKEN = '508099832:AAHaxtIpOdxLBKtvcMaZHVXKihKiUoHk0l0'

bot = telepot.DelegatorBot(TOKEN, [
    include_callback_query_chat_id(
        pave_event_space())(
        per_chat_id(), create_open, Shaq, timeout=10000
    ),
])
MessageLoop(bot).run_as_thread()
print('Messages since last login:')

while 1:
    time.sleep(10)