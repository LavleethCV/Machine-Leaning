import asyncio
import telebot
import requests
from bardapi import Bard
from bardapi.constants import SESSION_HEADERS


session = requests.session()
session.headers = SESSION_HEADERS
session.cookies.set(
    "__Secure-1PSID",
    "aAibYnnRKnkwyhH0H1SOLMiA7r2PwkSFX3imhbIdwBgkWZgqfuOyJEjcNrcknP499a9l2A.",
)
session.cookies.set(
    "__Secure-1PSIDTS",
    "sidts-CjEBSAxbGRfAffNsbD7_NExxK8RkgbcSX07VY3s0IFWug0pO5QNweVYLEU17dCktfMPYEAA",
)
session.cookies.set(
    "__Secure-1PSIDCC",
    "APoG2W9xHz0EuYsi-U5Mm0eyCAModdpx6_GZBQLV_JcR3S08VgUOLBFEWSzGkuMqd7bhtbDBZw",
)
bard = Bard(session=session, token_from_browser=True)

telegram_bot_token = "6403313898:AAFTXFSyOeM0BWIbafdQD5BTJp14a9mRtOI"
bot = telebot.TeleBot(telegram_bot_token, parse_mode="html")


@bot.message_handler(commands=["/hello", "/hey", "/good morning"])
def send_message(message):
    bot.reply_to(message, "Hello My name is BardBroker. How may i assist you?")


@bot.message_handler(func=lambda message: not message.text.startswith("/"))
def send_gpt(message):
    print("getting response")
    try:
        bot.send_chat_action(message.chat.id, "typing")
        response = bard.get_answer(message.text)
        bot.reply_to(message, response["content"])
    except Exception as e:
        bot.reply_to(message, str(e))


asyncio.run(bot.polling())
