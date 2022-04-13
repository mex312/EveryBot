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


@bot.message_handler()
def handle(message: telebot.types.Message):
    splitMessage = message.text.split(' ')

    if message.text[0] == '@':
        moduleName = splitMessage[0].removeprefix('@')

        for module in modules:
            if module.name.lower() == moduleName.lower():
                if len(splitMessage) >= 2:
                    if splitMessage[1] == "/help":
                        if len(splitMessage) >= 3:
                            core.send_message(message, module.help(splitMessage[2]))
                        else:
                            core.send_message(message, module.help())
                    else:
                        message.text = message.text.removeprefix(f"@{moduleName} ")
                        module.handle_message(message)
                break

    elif splitMessage[0] == "/help":

        reply: str = ""

        if (len(splitMessage) >= 2) and (splitMessage[1][0] == '/'):
            for module in modules:
                if module.help(splitMessage[1])[0] != '!':
                    reply += f"from {module.name}: {module.help(splitMessage[1])}\n"
        else:
            for module in modules:
                reply += f"@{module.name} /help\n"

        reply.removesuffix('\n')
        if reply != "":
            core.send_message(message, reply)
        else:
            core.send_message(message, "Can't find help for this command")

    else:
        for module in modules:
            module.handle_message(message)


for file in fullPaths:
    if os.path.isdir(file): dirs.append(file.removeprefix('Modules\\'))
    if os.path.isfile(file): files.append(file.removeprefix('Modules\\'))

for i in range(0, dirs.__len__()):
    modules += [importlib.import_module(f'Modules.{dirs[i]}.main').get_module(core)]

for module in modules:
    print(f"Module {module.name} initialized with commands: {module.help('')}")






bot.infinity_polling()
