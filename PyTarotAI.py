import requests
import json
import random
import pandas as pd
import xlrd
import os

# Major Arcana list
major_arcana = [
    "The Fool", "The Magician", "The High Priestess", "The Empress", "The Emperor",
    "The Hierophant", "The Lovers", "The Chariot", "Strength", "The Hermit",
    "Wheel of Fortune", "Justice", "The Hanged Man", "Death",
    "Temperance", "The Devil", "The Tower", "The Star",
    "The Moon", "The Sun", "Judgment", "The World"
]

# Minor Arcana list
minor_arcana = []
suits = ["Wands", "Cups", "Swords", "Pentacles"]
courts = ["King", "Queen", "Knight", "Page"]

for suit in suits:
    for court in courts:
        minor_arcana.append(suit + " " + court)
    for i in range(1, 11):  # Numeric cards from 1 to 10
        minor_arcana.append(suit + " " + str(i))

# Combine both lists into the Tarot deck
tarot_deck = major_arcana + minor_arcana

print("Welcome to the Cyber Tarot Shop!")
shuffle = input("Please type 'shuffle' to shuffle the deck, and silently think about your question: ")
random.shuffle(tarot_deck)

if shuffle == 'shuffle':
    print('The deck is shuffled!\n')
else:
    print("Although you didn't follow my instruction, I still shuffled the deck for you. Don't forget to give a good review.\n")

cut = input("Please type 'cut' to cut the deck, and silently think about your question: ")

if cut == 'cut':
    print('The deck is cut!\n')
else:
    print("Although you didn't follow my instruction, I still let you cut the deck. Don't forget to give a good review.\n")

i = input("How many cards would you like to draw (1, 3, 5, 7)? Please enter a number: ")
i = int(i)

formating = ""
if i == 1:
    formating = "Single Card Spread"
elif i == 3:
    formating = "Past-Present-Future Spread"
elif i == 5:
    formating = "Decision-Making Spread"
elif i == 7:
    formating = "Six-Pointed Star Spread"
else:
    formating = "Not belonging to any specific spread"

print("You have chosen the spread: 【" + formating + "】\n")

draw = []
for j in range(1, i + 1):
    card = input("Please choose a card number from 1 to 78 for the " + str(j) + " card, and avoid repeating the previous selections: ")
    card = int(card)
    draw.append("Card " + str(j) + ": " + tarot_deck[card])

draw = '\n'.join(draw)
flip = input("Now type 'flip' to reveal the drawn cards!")

if flip == 'flip':
    print("")
    print(draw)
else:
    print("Although you didn't follow my instruction, I still revealed the cards for you. Don't forget to give a good review.\n")
    print(draw)

question = input("Now, tell me your question: ")

openai.api_key = "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"

def interpret(prompt, model = "gpt-3.5-turbo", instruction = instruction):

    messages = [{"role": "system", "content": instruction},
                {"role": "user","content":prompt}]

    response = openai.ChatCompletion.create(
        model = model,
        messages = messages,
        tempreture = 0
        )
    return response.choice[0].message["content"]


print("Alright, let me put together a response for you~\n")

instruction = f"""
You are now playing the role of a Tarot master who is proficient in Tarot cards and serving customers at your own shop.

In the customer's input, it will include the cards they drew, their question, and the chosen spread.

In your response, you need to verbally interpret the meaning of each card based on its intention and position.

Then, based on the overall information from all cards and their positions, provide advice to the customer.

In your language, you should try to mimic the speech style of a Tarot master, including but not limited to using common terms used by Western Tarot readers/fortune tellers/wizards, using authentic colloquial expressions, incorporating feudal superstitions, and citing references from Western classic literature and theology.

You should appear friendly to the client while also showing that you are skilled, as you make a living from them.

Below are the interpretations for different spreads:///

Single Card Spread: Use only one card for divination, suitable for any question.

Past-Present-Future Spread: Suitable for yes-or-no questions, such as can or cannot, will or will not. Card 1 represents the past, card 2 the present, and card 3 the future.

Decision-Making Spread: This spread can be used for choice questions. Card 1 represents the current situation, card 2 the development after choosing option A, card 3 the development after choosing option B, card 4 the result after choosing option A, and card 5 the result after choosing option B.

Seven-Card Spread: Suitable for more complex comprehensive questions. Card 1 represents the past, card 2 the present, card 3 the future, card 4 provides advice, card 5 represents obstacles in the situation's development, card 6 represents the client's thoughts, and card 7 represents the outcome of the situation.

///
"""

prompt = f"""
Customer's Drawn Cards: {draw}

Customer's Question: {question}

Customer's Chosen Spread: {formating}

"""

response = call_openai_api(instruction, prompt)  # call openai API

print(response['choices'][0]['message']['content'])  # Output the returned value
print(response['usage']['total_tokens'])
