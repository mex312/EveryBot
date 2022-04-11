import telebot


class Unit:
    pass


class Core(Unit):
    modulesList = [Unit]
    bot = telebot.TeleBot("NO_TOKEN")

    def __init__(self, botToken):
        self.bot.token = botToken

    def DeleteMessage(self, message: telebot.types.Message):
        self.bot.delete_message(message_id=message.id, chat_id=message.chat.id)


class Module(Unit):
    name = "NAMELESS"
    core: Core

    def __init__(self, core):
        self.core = core
        self.core.modulesList += [self]

    def help(self):
        pass
