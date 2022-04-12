import telebot


class Unit:
    name = "UNIT"


class Core(Unit):
    modulesList: [Unit]
    bot = telebot.TeleBot("NO_TOKEN")

    def __init__(self, botToken: str):
        self.bot.token = botToken
        self.name = "CORE"

    def delete_message(self, message: telebot.types.Message):
        self.bot.delete_message(message_id=message.id, chat_id=message.chat.id)

    def add_module(self, module: Unit):
        self.modulesList += [module]


class Module(Unit):
    core: Core

    def __init__(self, core: Core, name: str = "NAMELESS"):
        self.core = core
        self.core.add_module(self)
        self.name = name

    def help(self):
        pass
