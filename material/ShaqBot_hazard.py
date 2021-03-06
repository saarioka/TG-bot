import time
import telepot
import random
import datetime
from Ruokalistat import Reaktori,Hertsi
from Vote import Votee
from telepot.loop import MessageLoop
from telepot.delegate import per_chat_id, create_open, pave_event_space
from telepot.namedtuple import InlineKeyboardButton, InlineKeyboardMarkup

msglist = []

class Lyrics(telepot.helper.ChatHandler):

    def __init__(self, *args, **kwargs):
        super(Lyrics, self).__init__(*args, **kwargs)
        with open('C:/Users/Santeri/Desktop/TelegramBot/lyrics.txt') as f:
            self._lyrics = f.readlines()
        with open('C:/Users/Santeri/Desktop/TelegramBot/lyrics.txt') as f:
            self._lyrics_all = f.read()
        self._lyrics = [x.strip() for x in self._lyrics]
        self._aloitusaika = time.time()-10
        #print("----------------------------------------------------------")
        self.sender.sendMessage("Shaq is in the house, boys!")


    def print_time_in(self, msg):
        apu =''
        if msg['chat']['id'] < 0:
            apu = msg['chat']['title'] + '|'
        print('[' + datetime.datetime.fromtimestamp(msg['date']).strftime('%H:%M:%S') + '] in  ' + apu  + msg['from']['first_name']+ ":", end=" ")
        
    def print_time_out(self, msg):
        apu = ''
        if msg['chat']['id'] < 0:
            apu = msg['chat']['title'] + '|'
        print('[' + datetime.datetime.fromtimestamp(msg['date']).strftime('%H:%M:%S') + '] out ' + apu  + msg['from']['first_name']+ ":", end=" ")

    def lyrics(self, msg):
        if msg['text'].lower() == '/lyrics':
            self.sender.sendMessage(self._lyrics_all)
            self.print_time_out(msg)
            print('/lyrics')
                    
    def kiitos(self, msg):
        self.sender.sendMessage('Kiitos')
        self.print_time_out(msg)
        print('kiitos')

    def greetings(self, msg):
        greetings_out = ['Helo','heyhey','Yooyoo', 'Hello', 'Hi', 'Heyyy', 'Hei','Hey','Moi','Moi','Moikka','Helou','What\'s up big man']
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
        
    def kysely(self,msg):

        my_inline_keyboard = [[
            InlineKeyboardButton(text='Hertsi', callback_data='/hertsi2'),
            InlineKeyboardButton(text='Reaktori', callback_data='/reaktori'),
        ], [
            InlineKeyboardButton(text='Kerro vitsi', callback_data='/asd'),
            InlineKeyboardButton(text='Tervehdi Roosaa', callback_data='Moi Roosa :)'),
        ]]

        keyboard = InlineKeyboardMarkup(inline_keyboard=my_inline_keyboard)
        bot.sendMessage(msg["chat"]["id"], "Description:", reply_markup=keyboard)

    def on_inline_query(self, msg):
        query_id, from_id, query_data = telepot.glance(msg, flavor='inline_query')
        self.answerCallbackQuery(query_id,text="testi")

    def on_chat_message(self, msg):

        try:
            if msg['date'] < (self._aloitusaika):
                self.print_time_in(msg)
                print (msg['text'])
            else:
                #Prints message to shell
                self.print_time_in(msg)
                print (msg['text'])
                
                #Adds message to list if there is no combo on other chat
                if len(msglist)>1:
                    if (not(msglist[-2]['text'].lower() == msglist[-1]['text'].lower()
                            and msglist[-2]['chat']['id'] == msglist[-1]['chat']['id']
                            and msg['chat']['id'] != msglist[-1]['chat']['id'])):
                        msglist.append(msg)
                else:
                    msglist.append(msg)

                #pilasib
                greetings_in = ['moi','hei shaq','yo','yoyo','helou', "moi shaq", "hei"]
                if (len(msglist)>2
                        and msglist[-3]['text'].lower() == msglist[-2]['text'].lower()
                        and msglist[-2]['text'].lower() != msglist[-1]['text'].lower()
                        and msglist[-3]['chat']['id'] == msglist[-2]['chat']['id']
                        and msglist[-2]['chat']['id'] == msglist[-1]['chat']['id']):
                    self.sender.sendMessage('pilasib')
                    self.print_time_out(msg)
                    print('pilasib')

                #lyrics
                elif msg['text'].lower() == '/lyrics':
                    self.lyrics(msg)

                #greetings
                elif msg['text'].lower() in greetings_in:
                    self.greetings(msg)
                    
                #kiitos
                elif msg['text'].lower().find('kiitos') == 0:
                    self.kiitos(msg)

                #Command:hertsi1
                elif msg['text'].lower().find('/hertsi') == 0:
                    self.sender.sendMessage(Hertsi.ruoka(1))
                    self.print_time_out(msg)
                    print('hertsi1')

                #Command:hertsi2
                elif msg['text'].lower().find('/hertsi2') == 0:
                    self.sender.sendMessage(Hertsi.ruoka(2))
                    self.print_time_out(msg)
                    print('hertsi2')

                #Command:Reaktori1
                elif msg['text'].lower().find('/reaktori') == 0:
                    self.sender.sendMessage(Reaktori.ruoka(1))
                    self.print_time_out(msg)
                    print('reaktori1')

                #Command:Reaktori2
                elif msg['text'].lower().find('/reaktori2') == 0:
                    self.sender.sendMessage(Reaktori.ruoka(2))
                    self.print_time_out(msg)
                    print('reaktori2')

                #kysely
                elif msg['text'].lower().find('/kysely') == 0:
                    self.kysely(msg)

                #vote
                elif msg['text'].lower().find('/vote') == 0:
                    Vote.Votee(msg)

                #Command:lyrics
                self.pilasib(msg)

                #Deletes old message(s) from list
                if len(msglist)>1 and msglist[-1]['text'].lower() != msglist[-2]['text'].lower():
                    del msglist[0:-2]
                    
        except KeyError:
            print ('Sticker/Picture/Other')


TOKEN = '508099832:AAHaxtIpOdxLBKtvcMaZHVXKihKiUoHk0l0'

bot = telepot.DelegatorBot(TOKEN, [
    pave_event_space()(
        per_chat_id(), create_open, Lyrics, timeout=100000
    ),
])
MessageLoop(bot).run_as_thread()
print ('Messages since last login:')

while 1:
    time.sleep(3)
