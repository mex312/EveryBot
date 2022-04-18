import telebot
from builtins import *


class Unit:
    name = "UNIT"


class Core(Unit):
    modulesList: [Unit] = []
    bot = telebot.TeleBot("NO_TOKEN")

    def __init__(self, botToken: str):
        self.bot.token = botToken
        self.name = "CORE"

    def delete_message(self, message: telebot.types.Message):
        self.bot.delete_message(message_id=message.id, chat_id=message.chat.id)

    def send_message(self, message: telebot.types.Message, module: Unit, text: str):
        self.bot.send_message(chat_id=message.chat.id, text=f"@{module.name}: {text}")

    def add_module(self, module: Unit):
        self.modulesList += [module]

    @staticmethod
    def is_arg_equals_type(arg: str, expectedType: type) -> bool:
        try:
            expectedType(arg)
            return True
        except:
            return False

    def throw_exception_wrong_type(self, message: telebot.types.Message, expectedType: type, receivedArg: str, module: Unit, command: str):
        try:
            int(receivedArg)
            self.send_message(message, module, f"ERR: Unexpected type in {command}. Expected type: [{expectedType.__name__}], received type: [int].\nType [@{module.name} /help {command}] to get help.")
        except:
            try:
                float(receivedArg)
                self.send_message(message, module, f"ERR: Unexpected type in {command}. Expected type: [{expectedType.__name__}], received type: [float].\nType [@{module.name} /help {command}] to get help.")
            except:
                if(receivedArg.lower() == "true") | (receivedArg.lower() == "false"):
                    self.send_message(message, module, f"ERR: Unexpected type in {command}. Expected type: [{expectedType.__name__}], received type: [bool].\nType [@{module.name} /help {command}] to get help.")
                else:
                    self.send_message(message, module, f"ERR: Unexpected type in {command}. Expected type: [{expectedType.__name__}], received type: [str].\nType [@{module.name} /help {command}] to get help.")

    def throw_exception_too_few_args(self, message: telebot.types.Message, expectedArgNum: int, receivedArgNum: int, module: Unit, command: str):
        self.send_message(message, module, f"ERR: Too few arguments in {command}. Expected argument number: {expectedArgNum}, received argument number: {receivedArgNum}.\nType [@{module.name} /help {command}] to get help.")


class Command(Unit):
    args: list[type]
    handler: type(lambda m, l: None)
    helpHandler: type(lambda m, h: None)
    core: Core
    module: Unit
    docStr: str

    def __init__(self, module: Unit, command: str, args: list[type], handler: type(lambda m, l: None), helpHandler: type(lambda m, h: None)):
        self.module = module
        self.core = module.core
        self.name = command
        self.args = args
        self.handler = handler
        self.helpHandler = helpHandler
        self.docStr = command
        for arg in args:
            self.docStr += f" [{arg.__name__}]"

    def handle(self, message: telebot.types.Message, command: str):
        splitComm = command.split(' ')
        if splitComm[0] == self.name:
            splitComm.remove(self.name)
            if len(splitComm) < len(self.args):
                self.core.throw_exception_too_few_args(message, len(self.args), len(splitComm), self.module, self.name)
                return
            for i in range(0, len(self.args)):
                if not(Core.is_arg_equals_type(splitComm[i], self.args[i])):
                    self.core.throw_exception_wrong_type(message, self.args[i], splitComm[i], self.module, self.name)
                    return
            self.handler(message, splitComm)
        elif splitComm[0] == "/help":
            self.helpHandler(message, self.docStr)


class BotModule(Unit):
    core: Core
    name: str = "NAMELESS"
    helpStr: str = "IT IS MODULE"
    commands: list[Command] = []

    def __init__(self, core: Core):
        self.core = core
        self.core.add_module(self)

    def add_new_command(self, command: str, args: list[type], handler: type(lambda m, l: None), helpHandler: type(lambda m, h: None)):
        self.commands += [Command(self, command, args, handler, helpHandler)]

    def add_command(self, command: Command):
        self.commands += [command]

    def get_command_list(self) -> list[str]:
        commandList: list[str] = []
        for command in self.commands:
            commandList += [command.name]
        return commandList

    def get_command_list_as_str(self) -> str:
        return str(self.get_command_list()).removesuffix(']').removeprefix('[').replace("'", '')

    def handle_poll(self, poll: telebot.types.Poll):
        pass

    def handle_inline(self, inline: telebot.types.InlineQuery):
        pass

    def handle_message(self, message: telebot.types.Message):
        pass

    def handle_channel_post(self, post: telebot.types.Message):
        pass

    def handle_callback_query(self, callback: telebot.types.CallbackQuery):
        pass

    def handle_chat_member(self, member: telebot.types.ChatMember):
        pass

    def handle_chosen_inline(self, inline: telebot.types.InlineQuery):
        pass

    def handle_edited_message(self, message: telebot.types.Message):
        pass

    def handle_poll_answer(self, poll: telebot.types.Poll):
        pass

    def handle_shipping_query(self, shipping: telebot.types.ShippingQuery):
        pass

    def handle_chat_join_request(self, request: telebot.types.ChatJoinRequest):
        pass

    def handle_edited_channel_post(self, post: telebot.types.Message):
        pass

    def handle_my_chat_member(self, member: telebot.types.ChatMember):
        pass

    def handle_pre_checkout_query(self, preCheckout: telebot.types.PreCheckoutQuery):
        pass
