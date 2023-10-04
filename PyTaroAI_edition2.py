import requests
import json
import random
import pandas as pd
import xlrd
import os
import openai
import time

# Set the API key for OpenAI
openai.api_key = "your openai api key"

def call_openai_api(instruction, prompt):
    """
    Calls the OpenAI API with a given instruction and prompt.
    Returns the API response.
    """
    model = "gpt-4"
    messages = [
        {"role": "system", "content": instruction},
        {"role": "user", "content": prompt}
    ]

    response = openai.ChatCompletion.create(
        model=model,
        messages=messages
    )

    return response

# Major Arcana cards (translated from Chinese)
major_arcana = [
    "The Fool", "The Magician", "The High Priestess", "The Empress", "The Emperor",
    "The Hierophant", "The Lovers", "The Chariot", "Strength", "The Hermit", 
    "Wheel of Fortune", "Justice", "The Hanged Man", "Death",
    "Temperance", "The Devil", "The Tower", "The Star", 
    "The Moon", "The Sun", "Judgment", "The World"
]

# Minor Arcana cards (translated from Chinese)
minor_arcana = []
suits = ["Wands", "Cups", "Swords", "Pentacles"]
courts = ["King", "Queen", "Knight", "Page"]
for suit in suits:
    for court in courts:
        minor_arcana.append(court + " of " + suit)
    for i in range(1, 11):  # Numbers 1-10
        minor_arcana.append(str(i) + " of " + suit)

# Combine the lists to create the full tarot deck
tarot_deck = major_arcana + minor_arcana

token = [0,0]

print("Welcome to the Cyber Tarot Shop!")
shuffle = input("Please enter 'Shuffle' to shuffle the cards while thinking of your question: ")
random.shuffle(tarot_deck)
if shuffle == 'Shuffle':
    print('The cards have been shuffled!\n')
else:
    print("Even though you didn't follow my instructions, I shuffled them for you. Remember to leave a positive review.\n")

cut = input("Please enter 'Cut' to cut the cards while thinking of your question: ")
if cut == 'Cut':
    print('The cards have been cut!\n')
else:
    print("Even though you didn't follow my instructions, I cut them for you. Remember to leave a positive review.\n")

i = input("How many cards do you wish to use for the spread? Please choose among (1, 3, 5, 7, 10) and enter the number:")
if not i.isdigit():
    print("Then let's draw a random card.\n")
    i = 1
i = int(i)
formatting = ""
formatting_meaning = ""
if i == 1:
    formatting = "Single Card Spread"
    formatting_meaning = "Only one card is used for divination, suitable for any question."
elif i == 3:
    formatting = "Past-Present-Future Spread"
    formatting_meaning = "Suitable for yes-or-no questions. The 1st card represents the past, the 2nd card the present, and the 3rd card the future."
elif i == 5:
    formatting = "Choice Spread"
    formatting_meaning = "Use this spread for multiple-choice questions. The 1st card represents the current situation, the 2nd card the outcome after choosing option A, the 3rd card the outcome after choosing option B, the 4th card the result after option A, and the 5th card the result after option B."
elif i == 7:
    formatting = "Hexagram Spread"
    formatting_meaning = "Suitable for more complex questions. The 1st card represents the past, the 2nd card the present, the 3rd card the future, the 4th card the advice, the 5th card the obstacles in the situation, the 6th card the querent's thoughts, and the 7th card the outcome of the situation."
elif i == 10:
    formatting = "Wheel of Tarot"
    formatting_meaning = "The 1st card represents past influences, the 2nd card the present situation, the 3rd card future trends, the 4th card inner strengths, the 5th card external influences, the 6th card past influences, the 7th card the present situation, the 8th card future trends, the 9th card inner strengths, and the 10th card external influences."
else:
    formatting = "Doesn't belong to any spread"

print("Your chosen spread is: 【" + formatting + "】\n")

draw = []
for j in range(1, i+1):
    card = input("Please choose a card number from 1 to 78, and don't repeat previous choices:")
    if not card.isdigit():
        card = random.choice(range(1,79))
        print("Then I'll draw a random card for you.")
    card = int(card)
    draw.append("Card " + str(j) + ": " + tarot_deck[card - 1])

draw = '\n'.join(draw)
flip = input('Now type “Flip” to reveal your cards:')
if flip == 'Flip':
    print("")
    print(draw)
else:
    print('Even though you didnt follow instructions, I still flipped the cards for you. Please leave a good review.\n')
    print(draw)

question = input('Now, tell me your question:')

tips = input('By the way, can you leave a tip?')

instruction_attitude = f'''

You need to perform precise semantic recognition. You'll analyze the user's response when asked, 'can you leave a tip?'
Based on the user's input, output the amount the user offered.

If the user explicitly mentions an amount, output that number.
If the user doesn't mention a number and gives a positive response, output 1.
If the user doesn't mention a number and is rude or offensive, output -1.
If the user doesn't mention a number and the tone is neutral or a polite refusal, output 0.

Examples:

Input: "Here's a billion."
Output: 1000000000

Input: "Get lost."
Output: -1

Input: "[Expletive], here's five bucks."
Output: 5

Input: "Alright."
Output: 1

Input: 
Output: 0

Input: 8
Output: 8

'''

tip_amount = 0

# Request tips from OpenAI API
response_tips = call_openai_api(instruction_attitude, tips)
attitude = ''

# Check if the tip amount is a positive or negative number
if response_tips['choices'][0]['message']['content'].isdigit():
    if int(response_tips['choices'][0]['message']['content']) > 0:
        attitude = 'The customer has given you a generous tip, so you should be friendly and warm, providing a positive explanation.'
        tip_amount = int(response_tips['choices'][0]['message']['content'])
    elif int(response_tips['choices'][0]['message']['content']) < 0:
        attitude = 'You are dealing with a difficult customer. To punish them, you will give the most negative explanation, even to the point of cursing.'

# Updating token consumption for tracking
token[0] = token[0] + response_tips['usage']['prompt_tokens']
token[1] = token[1] + response_tips['usage']['completion_tokens']

# Display the tip amount
print("\n" + "####### You've pledged a tip of: " + str(tip_amount) + " USD #######\n")

# Set the instructions for the Tarot card reader role-play scenario
instruction_tips = '''
You are now role-playing as a tarot card reader at a booth. Before interpreting the cards, you ask the customer for a tip.
Include the customer's response and the amount they offer in your answer.
After receiving the customer's reply, please continue in character, responding based on your tarot reader persona.
'''

# Provide a context of the customer's response
tip_situation = f'''
Customer's reply: {tips}
Tip amount given by the customer: {tip_amount}
'''

# Calling the OpenAI API with the role-play scenario
reaction = call_openai_api(instruction_tips, tip_situation)
token[0] = token[0] + reaction['usage']['prompt_tokens']
token[1] = token[1] + reaction['usage']['completion_tokens']

# Displaying the tarot reader's response to the customer's reply
print("\n" + reaction['choices'][0]['message']['content'])

# Setting instructions for the Tarot card reading 
instruction_explanation = """
You now need to role-play as a proficient tarot card reader serving customers in your shop.
You are familiar with the significance of each tarot card, clearly understand the symbols on each card,
and can decipher the unique meaning of each card based on their suits and numbers.
{attitude}

The customer's input will include the cards they've drawn, their question, the spread they've chosen, and the method of interpreting the spread.

In your response, you should verbally explain the symbolism of each card, their respective symbols, and their position, based on the customer's question.
Subsequently, synthesize the information from all cards and positions to offer suggestions. Your advice should be clear, specific, and can be creatively crafted.

In your language output, try to mimic the style of a tarot card reader, including but not limited to using terms commonly used by Western tarot card readers, 
using colloquial expressions, referencing feudal superstitions, and citing from Western classic literature and theological content.
"""

# Providing the customer's input context
prompt = f"""
Cards drawn by the customer: {draw}
Customer's question: {question}
Spread chosen by the customer: {formatting}
Method of reading the chosen spread: {formatting_meaning}
"""

# Calling OpenAI API with tarot card reading instructions
response_explanation = call_openai_api(instruction_explanation, prompt) # call openai API
token[0] = token[0] + response_explanation['usage']['prompt_tokens']
token[1] = token[1] + response_explanation['usage']['completion_tokens']
cost = (token[0] * 0.03 + token[1] * 0.06)
cost = cost/1000 + tip_amount

# Displaying the tarot reading and the total cost
print(response_explanation['choices'][0]['message']['content']) # Display the returned value
print("\n" + "Total charges for this session: " + str(cost) + " USD. Thank you for your patronage.")

