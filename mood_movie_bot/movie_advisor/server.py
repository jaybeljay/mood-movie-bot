import logging
import os

from aiogram import Bot, Dispatcher, executor, types
import aiohttp

from .services import get_mood_names, get_movie_by_mood
from .exceptions import MoodDoesNotExist


API_TOKEN = os.getenv('TELEGRAM_API_TOKEN')
API_URL = os.getenv('TELEGRAM_API_URL')

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

moods = get_mood_names()


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply(
        "Hi!\n"
        "I'm MoodMovieBot!\n"
        "Tell me what's your mood today and I will recommend you a nice movie to watch.\n"
        "Choices are:\n"
        "/giggly - comedy picks to keep your mood up\n"
        "/nasty - choose this if you want something wicked and kinky\n"
        "/dreamy - escape to surreal worlds\n"
        "/nerdy - for those who'd like to solve puzzles\n"
        "/relaxed - for those who wouldn't like to solve puzzles\n"
        "/bored - taste something new\n"
        "/stressed - comforting soup for your soul\n"
        "/okay - it doesn't matter\n"
        "/mad - feel like breaking something")


@dp.message_handler(commands=moods)
async def recommend_movie(message: types.Message):
    """
    This handler will be called when user sends one of the moods commands
    """
    try:
        command_mood = message.get_command()
        movie = get_movie_by_mood(command_mood)
    except MoodDoesNotExist:
        await message.answer("Sorry, I can't help. Try another mood.")
        return

    await message.answer(movie)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
