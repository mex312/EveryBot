import sys
sys.path.append('./SitePackages')
import telebot
import os
import importlib
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


@bot.message_handler()
def handle(message: telebot.types.Message):
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

    else:
        for module in modules:
            module.handle_message(message)


for file in fullPaths:
    if os.path.isdir(file): dirs.append(file.removeprefix('Modules\\'))
    if os.path.isfile(file): files.append(file.removeprefix('Modules\\'))

for i in range(0, dirs.__len__()):
    modules += [importlib.import_module(f'Modules.{dirs[i]}.main').get_module(core)]

for module in modules:
    print(f"Module {module.name} initialized with commands: {module.get_command_list_as_str()}")


bot.infinity_polling()
