import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InputSticker, Sticker
import re
def extract_emoji(text):
    # Emoji pattern from the emoji library
    emoji_pattern = re.compile(
        "[\U0001F600-\U0001F64F]"  # emoticons
        "|[\U0001F300-\U0001F5FF]"  # symbols & pictographs
        "|[\U0001F680-\U0001F6FF]"  # transport & map symbols
        "|[\U0001F1E0-\U0001F1FF]"  # flags (iOS)
        "|[\U00002702-\U000027B0]"  # dingbats
        "|[\U000024C2-\U0001F251]"  # enclosed characters
        "|[\U0001F900-\U0001F9FF]"  # supplemental symbols and pictographs
        "|[\U0001FA70-\U0001FAFF]"  # chess symbols and other additional symbols
        "+", flags=re.UNICODE
    )
    
    # Search for emojis in the text
    emojis_found = emoji_pattern.findall(text)
    
    if emojis_found:
        return emojis_found[0]  # Return the first emoji found
    else:
        return None  # No emoji found
input_string = "Hello 😊! How are you?"
target_emoji = extract_emoji(input_string)
# Set up logging
logging.basicConfig(level=logging.INFO)

# Replace with your bot token
API_TOKEN = '7596140425:AAEsNVUHyUZAjH_hoLN35c77Gl_dvUfsPzg'
bot = Bot(token=API_TOKEN)
dp = Dispatcher()
# Command handler to get sticker pack
var_emoji= "👍"
@dp.message()
async def get_sticker_pack(message: types.Message):
    sticker_set = await bot.get_sticker_set("f293b5c7_1ad4_41fc_8a95_a4a3dc5a14cf_by_sticat_bot")
    await message.answer_sticker(next((sticker for sticker in sticker_set.stickers if sticker.emoji == target_emoji), None).file_id)

async def main():
    # Start polling
    await dp.start_polling(bot)

if __name__ == '__main__':
    # Run the bot
    asyncio.run(main())