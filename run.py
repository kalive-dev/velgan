import time
import requests
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InputFile, StickerSet, FSInputFile
from aiogram.methods import DeleteWebhook
import asyncio
import markovify
import aiofiles
from elevenlabs import save, Voice, VoiceSettings
from elevenlabs.client import ElevenLabs
import sqlite3
import random
import requests 
from parse import extract_emoji


API_TOKEN = '7596140425:AAEsNVUHyUZAjH_hoLN35c77Gl_dvUfsPzg'
ELEVENLABS_API_KEY = 'sk_1a9d3b4d46dc0555a59ffa7ca96438f420c574470b0f50e9'
# Create bot instance
bot = Bot(token=API_TOKEN)
dp = Dispatcher()
client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
# Connect to the database (or create if it doesn't exist)
conn = sqlite3.connect('chat_settings.db')
cursor = conn.cursor()

# Create table to store percentage settings for each chat
cursor.execute('''
    CREATE TABLE IF NOT EXISTS chat_settings (
        chat_id INTEGER PRIMARY KEY,
        percentage INTEGER DEFAULT 100
    )
''')
conn.commit()

# Load the Markov chain model from the velganMessages.txt file
with open("velganMessages.txt", "r", encoding="utf-8") as f:
    text = f.read()

# Build the Markov chain model
markov_model = markovify.NewlineText(text)
print("Markov model generated!")


# /start command handler
@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    await message.answer("прівіт! я Вельганотрон, мене побудували найкращі кішники цього світу")

# Command to set percentage for message sending
@dp.message(Command("percentage"))
async def set_percentage(message: types.Message):
    try:
        # Extract the percentage value from the message
        percentage = int(message.text.split()[1])
        
        if 0 <= percentage <= 100:
            chat_id = message.chat.id
            
            # Save or update percentage setting in the database
            cursor.execute('''
                INSERT INTO chat_settings (chat_id, percentage) 
                VALUES (?, ?)
                ON CONFLICT(chat_id) 
                DO UPDATE SET percentage = excluded.percentage
            ''', (chat_id, percentage))
            conn.commit()
            
            await message.answer(f"Встановлено частоту надсилання повідомлень: {percentage}%")
        else:
            await message.answer("Будь ласка, введіть відсоток у межах від 0 до 100.")
    except (ValueError, IndexError):
        await message.answer("Будь ласка, введіть правильний формат: /percentage {відсоток}")

@dp.message(F.text == "вельган стікер")
async def whatt(message: types.Message):
    sticker_set = await bot.get_sticker_set("f293b5c7_1ad4_41fc_8a95_a4a3dc5a14cf_by_sticat_bot")
    sticker_count = len(sticker_set.stickers)  # Use len() to get the number of stickers
    await message.answer_sticker(sticker=sticker_set.stickers[random.randint(0, sticker_count - 1)].file_id)

# @dp.message(F.text == "вельган про що думаєш" or Command("imagine"))
# async def imagine(message: types.Message):
#     generated_message = markov_model.make_sentence(tries=100)
    
#     response = client_openai.images.generate(
#         model="dall-e-3",
#         prompt=generated_message,
#         size="1024x1024",
#         quality="standard",
#         n=1,
#     )
#     image_url = response.data[0].url
#     if response.status_code == 200:
#         await message.answer_photo(image_url)
#     else:
#         await message.answer("Error: Unable to generate image.")



    
@dp.message()
async def generate_message(message: types.Message):
    chat_id = message.chat.id

    # Get percentage setting for the chat (default 100 if not set)
    cursor.execute('SELECT percentage FROM chat_settings WHERE chat_id = ?', (chat_id,))
    result = cursor.fetchone()
    percentage = result[0] if result else 100

    if random.randint(1, 100) <= percentage:
        # Generate a random sentence using the Markov chain model
        generated_message = markov_model.make_sentence(tries=100)
        # await bot.send_chat_action(action="record_voice", chat_id=chat_id)

        if generated_message:
            # Extract emoji from the generated message
            target_emoji = extract_emoji(generated_message)  # This needs to be defined before printing

            print(f"Generated message: {generated_message}, targeted emoji: {target_emoji}")
            # audio = client.generate(
            #     text=generated_message,
            #     voice=Voice(
            #         voice_id="iP95p4xoKVk53GoZ742B",
            #         settings = VoiceSettings(stability=0.9, style=0.12, similarity_boost=0.5, use_speaker_boost=True)
            #     ),
            #     model="eleven_multilingual_v2",
            # )
            
            # save(audio, "output.mp3")
            # await bot.send_chat_action(action="upload_voice", chat_id=chat_id)
            # voice_file = types.FSInputFile('output.mp3')
            # await message.answer_voice(voice_file)
            await message.answer(generated_message)

            # Send a sticker if an emoji is found
            if target_emoji:
                sticker_set = await bot.get_sticker_set("f293b5c7_1ad4_41fc_8a95_a4a3dc5a14cf_by_sticat_bot")
                matching_sticker = next((sticker for sticker in sticker_set.stickers if sticker.emoji == target_emoji), None)
                if matching_sticker:
                    await message.answer_sticker(matching_sticker.file_id)
        else:
            await message.answer("Sorry, I couldn't generate a message at this time.")
    else:
        print(f"Skipped message generation for chat {chat_id} due to percentage setting.")


async def main():
    await bot(DeleteWebhook(drop_pending_updates=True))
    # Start polling
    await dp.start_polling(bot)

if __name__ == '__main__':
    # Run the bot
    asyncio.run(main())