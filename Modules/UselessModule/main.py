import telebot
from every_bot import Module, Core


class UselessModule(Module):
    name = 'UselessModule'
    bot: telebot.TeleBot

    def __init__(self, core: Core):
        super().__init__(core)

        self.bot = self.core.bot

        @self.bot.message_handler(commands=['hello'])
        def hello(message: telebot.types.Message):
            core.delete_message(message)
            self.bot.send_message(chat_id=message.chat.id, text="Hello!")

        @self.bot.message_handler()
        def repeater(message: telebot.types.Message):
            if message.text[0] != '/':
                core.delete_message(message)
                self.bot.send_message(chat_id=message.chat.id, text=message.text)

    """Bot's core will call it when user type /help"""
    """It will merge like '[yourReturn] from [UselessModule]' """
    def help(self):
        return '/hello'


def get_module(core):
    return UselessModule(core)
