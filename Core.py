import sys
sys.path.append('./SitePackages')
import telebot
import os
import importlib
from every_bot import Module, Core

dirFiles = os.listdir('Modules')
fullPaths = map(lambda name: os.path.join('Modules', name), dirFiles)

dirs = []
files = []

core = Core('5105437710:AAHItsntSLpyZNb2fa4JHjXg0LFa9fiWCTU')
bot: telebot.TeleBot
bot = core.bot
bot.parse_mode = None

modules: [Module] = []


@bot.message_handler(commands=['help'])
def sendHelp(message: telebot.types.Message):
    reply = "There's the commands you can use:"
    for module in modules:
        reply += f"\n{module.help()} from {module.name}"
    core.delete_message(message)
    core.bot.send_message(chat_id=message.chat.id, text=reply)


for file in fullPaths:
    if os.path.isdir(file): dirs.append(file.removeprefix('Modules\\'))
    if os.path.isfile(file): files.append(file.removeprefix('Modules\\'))

for i in range(0, dirs.__len__()):
    modules += [importlib.import_module(f'Modules.{dirs[i]}.main').get_module(core)]

for module in modules:
    print(f"Module {module.name} initialized with commands: {None}")







bot.infinity_polling()
