import copy
import sys
sys.path.append('./SitePackages')
import telebot
import os
import importlib
from math import *
from every_bot import *

MODULE_LIST_SIZE: int = 10
MODULE_COMMANDS_LIST_SIZE: int = 10

dirFiles = os.listdir('Modules')
fullPaths = map(lambda name: os.path.join('Modules', name), dirFiles)

dirs = []
files = []

core = Core('5105437710:AAHItsntSLpyZNb2fa4JHjXg0LFa9fiWCTU')
bot: telebot.TeleBot
bot = core.bot
bot.parse_mode = None

modules: [BotModule] = []


coreModule = BotModule(core)
coreModule.name = "Core"


def create_modules_list_keyboard(page: int) -> telebot.types.InlineKeyboardMarkup:
    keyboard = telebot.types.InlineKeyboardMarkup()
    buttons: list[telebot.types.InlineKeyboardButton] = []
    for i in range(page * MODULE_LIST_SIZE, (page+1) * MODULE_LIST_SIZE):
        if (i < len(modules)) and (i >= 0):
            buttons += [telebot.types.InlineKeyboardButton(text=f"@{modules[i].name}", callback_data=f"@{modules[i].name}:/help")]
        else:
            buttons += [telebot.types.InlineKeyboardButton(text=" ", callback_data="NoneOnModuleList")]
        if i % 2 == 1:
            keyboard.add(*buttons)
            buttons = []
    buttons: list[telebot.types.InlineKeyboardButton] = []
    if page > 0:
        buttons += [telebot.types.InlineKeyboardButton(text="<---", callback_data=f"SetPageOnModuleList:{page - 1}")]
    else:
        buttons += [telebot.types.InlineKeyboardButton(text="<---", callback_data=f"SetPageOnModuleList:{page}")]
    if page < ceil(float(len(modules)) / MODULE_LIST_SIZE) - 1:
        buttons += [telebot.types.InlineKeyboardButton(text="--->", callback_data=f"SetPageOnModuleList:{page + 1}")]
    else:
        buttons += [telebot.types.InlineKeyboardButton(text="--->", callback_data=f"SetPageOnModuleList:{page}")]
    keyboard.add(*buttons)
    return keyboard


def create_commands_list_keyboard(page: int, module: BotModule) -> telebot.types.InlineKeyboardMarkup:
    keyboard = telebot.types.InlineKeyboardMarkup()
    buttons: list[telebot.types.InlineKeyboardButton] = []
    commands: list[str] = module.get_command_list()
    for i in range(page * MODULE_COMMANDS_LIST_SIZE, (page+1) * MODULE_COMMANDS_LIST_SIZE):
        if (i < len(commands)) and (i >= 0):
            buttons += [telebot.types.InlineKeyboardButton(text=commands[i], callback_data=f"@{module.name}:/help {commands[i]}")]
        else:
            buttons += [telebot.types.InlineKeyboardButton(text=" ", callback_data="NoneOnModuleCommandsList")]
        if i % 2 == 1:
            keyboard.add(*buttons)
            buttons = []
    buttons: list[telebot.types.InlineKeyboardButton] = []
    if page > 0:
        buttons += [telebot.types.InlineKeyboardButton(text="<---", callback_data=f"SetPageOnModuleCommandsList:{page - 1}@{module.name}")]
    else:
        buttons += [telebot.types.InlineKeyboardButton(text="<---", callback_data=f"SetPageOnModuleCommandsList:{page}@{module.name}")]
    if page < ceil(float(len(commands)) / MODULE_COMMANDS_LIST_SIZE) - 1:
        buttons += [telebot.types.InlineKeyboardButton(text="--->", callback_data=f"SetPageOnModuleCommandsList:{page + 1}@{module.name}")]
    else:
        buttons += [telebot.types.InlineKeyboardButton(text="--->", callback_data=f"SetPageOnModuleCommandsList:{page}@{module.name}")]
    keyboard.add(*buttons)
    return keyboard


@bot.message_handler()
def handle_any_message(message: telebot.types.Message):
    splitMessage = message.text.split(' ')

    if message.text[0] == '@':
        moduleName = splitMessage[0].removeprefix('@')

        for module in modules:
            if module.name.lower() == moduleName.lower():
                if len(splitMessage) >= 2:
                    if splitMessage[1] == "/help":
                        if (len(splitMessage) >= 3) and (splitMessage[2][0] == "/"):
                            found = False
                            for command in module.commands:
                                if command.name == splitMessage[2]:
                                    found = True
                                    command.handle(message, "/help")
                                    break
                            if not found:
                                core.send_message(message, module, "I don't have such command")
                        else:
                            core.send_message(message, module, f"{module.helpStr}\nThere's all commands from this module:\n{module.get_command_list_as_str()}")
                            bot.send_message(message.chat.id, f"@{module.name}: Choose command to get help", reply_markup=create_commands_list_keyboard(0, module))
                    else:
                        message.text = message.text.removeprefix(f"@{moduleName} ")
                        module.handle_message(message)
                break

    elif splitMessage[0] == "/help":

        reply: str = ""

        if (len(splitMessage) >= 2) and (splitMessage[1][0] == '/'):
            found = False
            for module in modules:
                for command in module.commands:
                    if splitMessage[1] == command.name:
                        command.handle(message, '/help')
                        found = True
            if not found:
                core.send_message(message, coreModule, "Can't find such command")
        else:
            reply += "You can get help for each module with command [@[ModuleName] /help]\nThere's all installed modules:\n"
            for module in modules:
                reply += f"@{module.name}\n"

            reply.removesuffix('\n')
            core.send_message(message, coreModule, reply)

            bot.send_message(message.chat.id, "@Core: Choose module to get help", reply_markup=create_modules_list_keyboard(0))

    else:
        for module in modules:
            module.handle_message(message)


@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call: telebot.types.CallbackQuery):
    if call.data.find("SetPageOnModuleList:") != -1:
        keyboard: telebot.types.InlineKeyboardMarkup = create_modules_list_keyboard(int(call.data.removeprefix("SetPageOnModuleList:")))
        try:
            bot.edit_message_reply_markup(call.message.chat.id, call.message.id, reply_markup=keyboard)
        except:
            pass
        bot.answer_callback_query(call.id)

    elif call.data == "NoneOnModuleList":
        bot.answer_callback_query(call.id)

    elif call.data.find("SetPageOnModuleCommandsList:") != -1:
        splitData = call.data.removeprefix("SetPageOnModuleCommandsList:").split('@')
        for module in modules:
            if module.name.lower == splitData[1].lower():
                keyboard = create_commands_list_keyboard(int(splitData[0]), module)
                try:
                    bot.edit_message_reply_markup(call.message.chat.id, call.message.id, reply_markup=keyboard)
                except:
                    pass
                break
        bot.answer_callback_query(call.id)

    else:
        if call.data[0] == '@':
            if (len(call.data.split(':')) >= 2) and (call.data.split(':')[1].split(' ')[0] == "/help"):
                message = copy.copy(call.message)
                message.text = f"{call.data.split(':')[0]} {call.data.split(':')[1]}"
                handle_any_message(message)
            else:
                for module in modules:
                    if module.name == call.data.split(':')[0].removeprefix('@'):
                        module.handle_callback_query(call)
        else:
            for module in modules:
                module.handle_callback_query(call)
        bot.answer_callback_query(call.id)


for file in fullPaths:
    if os.path.isdir(file): dirs.append(file.removeprefix('Modules\\'))
    if os.path.isfile(file): files.append(file.removeprefix('Modules\\'))

for i in range(0, dirs.__len__()):
    modules += [importlib.import_module(f'Modules.{dirs[i]}.main').get_module(core)]

for module in modules:
    print(f"Module {module.name} initialized with commands: {module.get_command_list_as_str()}")

bot.polling()