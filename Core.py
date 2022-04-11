import sys
sys.path.append('./SitePackages')
import telebot
import os
import importlib
from EveryBot.types import Module, Core

dirfiles = os.listdir('Modules')
fullpaths = map(lambda name: os.path.join('Modules', name), dirfiles)

dirs = []
files = []

core = Core('5105437710:AAHItsntSLpyZNb2fa4JHjXg0LFa9fiWCTU')
core.bot.parse_mode = None

modules: [Module]
modules = []

for file in fullpaths:
    if os.path.isdir(file): dirs.append(file.removeprefix('Modules\\'))
    if os.path.isfile(file): files.append(file.removeprefix('Modules\\'))

for i in range(0, dirs.__len__()):
    modules += [importlib.import_module(f'Modules.{dirs[i]}.main').GetModule(core)]

for module in modules:
    print(f"Module {module.name} initialized with commands: {None}")

bot: telebot.TeleBot
bot = core.bot


@bot.message_handler(commands=['help'])
def sendHelp(message: telebot.types.Message):
    reply = "There's the commands you can use:"
    for module in modules:
        reply += f"\n{module.help()} from {module.name}"
    core.DeleteMessage(message)
    core.bot.send_message(chat_id=message.chat.id, text=reply)


bot.infinity_polling()
