from dotenv import load_dotenv
import os
from gemini import get_response
import time
import discord


load_dotenv()
api_key = os.getenv("API_KEY")
intents = discord.Intents.default()
intents.typing = True
intents.messages = True
intents.message_content = True
discord_token = os.getenv("DISCORD_TOKEN")
class Bot():

    def __init__(self, api_key):
        self.api_key = api_key
        self.history = []

    def get_bot_response(self, user_input):

        self.history = self.history[-10:]
        while True:
            try:
                response = get_response(api_key, user_input, self.history)
                dict_input = {"role": "user", "parts": [user_input]}
                dict_response = {"role": "model", "parts": [response]}
                self.history.append(dict_input)
                self.history.append(dict_response)
                print(f"User: {user_input}\nDAMU: {response}")
                return response
            except Exception as e:
                print(f"ERROR: {e}")
                time.sleep(2)


client = discord.Client(intents=intents)
bot = Bot(api_key=api_key)
@client.event
async def on_ready():
    print(f"We have logged in as a {client}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if "damu" in message.content.lower() or str(client.user.id) in message.content:
        prompt = message.content
        if str(client.user.id) in prompt:
            prompt = prompt.replace(f"<@{str(client.user.id)}>", "Damu")
        bot_resp = bot.get_bot_response(prompt)
        await message.channel.send(bot_resp)

client.run(discord_token)



