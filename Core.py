import copy
import sys
sys.path.append('./SitePackages')
import telebot
import os
import importlib
from math import *
from every_bot import BotModule, Core

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

usersModuleListPage: dict[str: int] = {}
usersModuleListLastMessage: dict[str: telebot.types.Message] = {}


def create_modules_list_keyboard(page: int) -> telebot.types.InlineKeyboardMarkup:
    keyboard = telebot.types.InlineKeyboardMarkup()
    buttons: list[telebot.types.InlineKeyboardButton] = []
    for i in range(page * 10, (page+1) * 10):
        if (i < len(modules)) and (i >= 0):
            buttons += [telebot.types.InlineKeyboardButton(text=f"@{modules[i].name}", callback_data='@' + modules[i].name)]
        else:
            buttons += [telebot.types.InlineKeyboardButton(text=" ", callback_data="NoneOnModuleList")]
        if i % 2 == 1:
            keyboard.add(*buttons)
            buttons = []
    buttons: list[telebot.types.InlineKeyboardButton] = []
    if page > 0:
        buttons += [telebot.types.InlineKeyboardButton(text="<---", callback_data=f"SetPageOnModuleList{page - 1}")]
    else:
        buttons += [telebot.types.InlineKeyboardButton(text="<---", callback_data=f"SetPageOnModuleList{page}")]
    if page < ceil(float(len(modules)) / 10) - 1:
        buttons += [telebot.types.InlineKeyboardButton(text="--->", callback_data=f"SetPageOnModuleList{page + 1}")]
    else:
        buttons += [telebot.types.InlineKeyboardButton(text="--->", callback_data=f"SetPageOnModuleList{page}")]
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

            usersModuleListLastMessage[message.from_user.username] = bot.send_message(message.chat.id, "CHOOSE", reply_markup=create_modules_list_keyboard(0))
            usersModuleListPage[message.from_user.username] = 0

    else:
        for module in modules:
            module.handle_message(message)


@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call: telebot.types.CallbackQuery):
    if call.data == "NextPageOnModuleList":
        if usersModuleListPage[call.from_user.username] < ceil(float(len(modules)) / 10) - 1:
            usersModuleListPage[call.from_user.username] += 1
        keboard: telebot.types.InlineKeyboardMarkup = create_modules_list_keyboard(usersModuleListPage[call.from_user.username])
        message: telebot.types.Message = usersModuleListLastMessage[call.from_user.username]
        try:
            bot.edit_message_reply_markup(message.chat.id, message.id, reply_markup=keboard)
        except:
            pass
        bot.answer_callback_query(call.id)

    elif call.data == "PrevPageOnModuleList":
        if usersModuleListPage[call.from_user.username] > 0:
            usersModuleListPage[call.from_user.username] -= 1
        keboard: telebot.types.InlineKeyboardMarkup = create_modules_list_keyboard(usersModuleListPage[call.from_user.username])
        message: telebot.types.Message = usersModuleListLastMessage[call.from_user.username]
        try:
            bot.edit_message_reply_markup(message.chat.id, message.id, reply_markup=keboard)
        except:
            pass
        bot.answer_callback_query(call.id)

    elif call.data == "NoneOnModuleList":
        bot.answer_callback_query(call.id)

    else:
        for module in modules:
            if call.data == '@' + module.name:
                message = copy.copy(call.message)
                message.text = f"@{module.name} /help"
                handle_any_message(message)
        bot.answer_callback_query(call.id)

for file in fullPaths:
    if os.path.isdir(file): dirs.append(file.removeprefix('Modules\\'))
    if os.path.isfile(file): files.append(file.removeprefix('Modules\\'))

for i in range(0, dirs.__len__()):
    modules += [importlib.import_module(f'Modules.{dirs[i]}.main').get_module(core)]

for module in modules:
    print(f"Module {module.name} initialized with commands: {module.get_command_list_as_str()}")


bot.infinity_polling()
