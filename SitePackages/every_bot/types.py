import telebot


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

    def send_message(self, message: telebot.types.Message, text: str):
        self.bot.send_message(chat_id=message.chat.id, text=text)

    def add_module(self, module: Unit):
        self.modulesList += [module]

    @staticmethod
    def is_arg_equals_type(arg: str, expectedType: type) -> bool:
        try:
            expectedType(arg)
            return True
        except:
            return False

    @staticmethod
    def throw_exception_wrong_type(expectedType: type, receivedArg: str, moduleName: str, command: str) -> str:
        try:
            int(receivedArg)
            return f"ERR: Unexpected type in {command}. Expected type: [{expectedType.__name__}], received type: [int].\nType [@{moduleName} /help {command}] to get help."
        except:
            try:
                float(receivedArg)
                return f"ERR: Unexpected type in {command}. Expected type: [{expectedType.__name__}], received type: [float].\nType [@{moduleName} /help {command}] to get help."
            except:
                if(receivedArg.lower() == "true") | (receivedArg.lower() == "false"):
                    return f"ERR: Unexpected type in {command}. Expected type: [{expectedType.__name__}], received type: [bool].\nType [@{moduleName} /help {command}] to get help."
                else:
                    return f"ERR: Unexpected type in {command}. Expected type: [{expectedType.__name__}], received type: [str].\nType [@{moduleName} /help {command}] to get help."

    @staticmethod
    def throw_exception_too_few_args(expectedArgNum: int, receivedArgNum: int, moduleName: str, command: str):
        return f"ERR: Too few arguments in {command}. Expected argument number: {expectedArgNum}, received argument number: {receivedArgNum}.\nType [@{moduleName} /help {command}] to get help."


class Module(Unit):
    core: Core
    name: str = "NAMELESS"

    def __init__(self, core: Core):
        self.core = core
        self.core.add_module(self)

    def help(self, command: str = "") -> str:
        pass

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
