import telebot
from every_bot import *


class MathMod(BotModule):
    name = "MathMod"
    helpStr = "This module can do some math operations for you"
    bot: telebot.TeleBot
    commands: list[Command] = []

    def hello_handler(self, message: telebot.types.Message, args: list[str]):
        self.core.send_message(message, self, f"Hello, {message.from_user.username}!")

    def hello_help_handler(self, message: telebot.types.Message, docStr: str):
        self.core.send_message(message, self, docStr + "\nIt will say hello to you :3")

    def summ_handler(self, message: telebot.types.Message, args: list[str]):
        self.core.send_message(message, self, f"The answer is {float(args[0]) + float(args[1])}")

    def summ_help_handler(self, message: telebot.types.Message, docStr: str):
        self.core.send_message(message, self, docStr + "\nIt will summ two numbers for you.")

    def subt_handler(self, message: telebot.types.Message, args: list[str]):
        self.core.send_message(message, self, f"The answer is {float(args[0]) - float(args[1])}")

    def subt_help_handler(self, message: telebot.types.Message, docStr: str):
        self.core.send_message(message, self, docStr + "\nIt will subtract two numbers for you.")

    def __init__(self, core: Core):
        super().__init__(core)

        self.bot = self.core.bot

        self.add_new_command("/hello", [], self.hello_handler, self.hello_help_handler)
        self.add_new_command("/summ", [float, float], self.summ_handler, self.summ_help_handler)
        self.add_new_command("/subt", [float, float], self.subt_handler, self.subt_help_handler)

    def handle_message(self, message: telebot.types.Message):
        splitMessage = message.text.split(' ')

        for command in self.commands:
            if command.name == splitMessage[0]:
                command.handle(message, message.text)


def get_module(core):
    return MathMod(core)
