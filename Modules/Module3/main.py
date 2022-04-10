import telebot
import EveryBot


class NONE_MODULE(EveryBot.Module.Module):
    name = 'NONE_MODULE'
    bot: telebot.TeleBot

    def __init__(self, core):
        super().__init__(core)

        self.bot = self.core.bot

        @self.bot.message_handler(commands=['NONE'])
        def NONE(message: telebot.types.Message):
            self.bot.delete_message(message_id=message.id, chat_id=message.chat.id)

    def help(self):
        pass


def GetModule(core):
    return NONE_MODULE(core)
