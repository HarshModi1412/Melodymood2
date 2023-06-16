import os
from bard import chatbot

token = open('token.txt','r').read().strip('\n').strip()

bot = chatbot(token)

prompt = input("How can i help you?")

output = bot.ask(prompt)['content']

print(output)
