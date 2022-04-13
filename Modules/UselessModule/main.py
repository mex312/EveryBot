import telebot
from every_bot import Module, Core


class MathMod(Module):
    name = 'MathMod'
    bot: telebot.TeleBot

    def __init__(self, core: Core):
        super().__init__(core)

        self.bot = self.core.bot

    def handle_message(self, message: telebot.types.Message):
        splitMessage = message.text.split(' ')

        if splitMessage[0] == "/hello":
            self.core.send_message(message, "Hello!")

        elif splitMessage[0] == "/summ":
            if len(splitMessage) < 3:
                self.core.send_message(message, self.core.throw_exception_too_few_args(2, len(splitMessage) - 1, self.name, "/summ"))
                return
            if not(self.core.is_arg_equals_type(splitMessage[1], float)):
                self.core.send_message(message, self.core.throw_exception_wrong_type(float, splitMessage[1], self.name, "/summ"))
            if not(self.core.is_arg_equals_type(splitMessage[2], float)):
                self.core.send_message(message, self.core.throw_exception_wrong_type(float, splitMessage[2], self.name, "/summ"))
            self.core.send_message(message, f"The answer is {float(splitMessage[1]) + float(splitMessage[2])}")

        elif splitMessage[0] == "/subt":
            if len(splitMessage) < 3:
                self.core.send_message(message, self.core.throw_exception_too_few_args(2, len(splitMessage) - 1, self.name, "/subt"))
                return
            if not(self.core.is_arg_equals_type(splitMessage[1], float)):
                self.core.send_message(message, self.core.throw_exception_wrong_type(float, splitMessage[1], self.name, "/subt"))
                return
            if not(self.core.is_arg_equals_type(splitMessage[2], float)):
                self.core.send_message(message, self.core.throw_exception_wrong_type(float, splitMessage[2], self.name, "/subt"))
                return
            self.core.send_message(message, f"The answer is {float(splitMessage[1]) - float(splitMessage[2])}")

    def help(self, command: str = "") -> str:
        if command == "":
            return "/hello, /summ, /subt"

        elif command == "/hello":
            return "/hello\nIt will say hello to you"

        elif command == "/summ":
            return "/summ [float] [float]\nIt will summ two numbers for you"

        elif command == "/subt":
            return "/subt [float] [float]\nIt will subtract two numbers for you"

        else:
            return "!I don't have command like this"


def get_module(core):
    return MathMod(core)
