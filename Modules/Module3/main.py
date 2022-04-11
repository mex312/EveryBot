import random

import telebot
from EveryBot.types import Module, Core
import time


class USELESS_MODULE(Module):
    name = 'USELESS_MODULE'
    bot: telebot.TeleBot
    phrases = ["Hello", "Hi", "Good day time", "Go f*ck yourself"]
    coin = ['tail', 'head']

    def __init__(self, core: Core):
        super().__init__(core)

        self.bot = self.core.bot

        @self.bot.message_handler(commands=['NONE'])
        def NONE(message: telebot.types.Message):
            core.DeleteMessage(message)

        @self.bot.message_handler(commands=['gettime'])
        def GetTime(message: telebot.types.Message):
            core.DeleteMessage(message)
            self.bot.send_message(chat_id=message.chat.id, text=str(time.strftime("%X\n%x")))

        @self.bot.message_handler(commands=['phrase'])
        def GetPhrase(message: telebot.types.Message):
            core.DeleteMessage(message)
            self.bot.send_message(chat_id=message.chat.id, text=random.choice(self.phrases))

        @self.bot.message_handler(commands=['coinflip'])
        def DropCoin(message: telebot.types.Message):
            core.DeleteMessage(message)
            self.bot.send_message(chat_id=message.chat.id, text=str(random.choice(self.coin)))

    def help(self):
        return '/gettime, /NONE, /phrase, /coinflip'


def GetModule(core):
    return USELESS_MODULE(core)
