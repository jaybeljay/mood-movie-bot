import logging
import os

from aiogram import Bot, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.webhook import SendMessage
from aiogram.utils.executor import start_webhook

from mood_movie_bot.movie_advisor.services import get_mood_names, get_movie_by_mood
from mood_movie_bot.movie_advisor.exceptions import MoodDoesNotExist


API_TOKEN = os.getenv('TELEGRAM_API_TOKEN')
HEROKU_TOKEN = os.getenv('HEROKU_TOKEN')

WEBHOOK_HOST = 'https://mood-movie-bot.herokuapp.com'
WEBHOOK_PATH = HEROKU_TOKEN
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = os.getenv('PORT', 5000)

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

moods = get_mood_names()


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.answer(
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
        movie = get_movie_by_mood(command_mood[1:])
    except MoodDoesNotExist:
        return SendMessage(message.chat.id, "Sorry, I can't help. Try another mood.")
        return

    return SendMessage(message.chat.id, movie)
    
    
async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_URL)
    
    
async def on_shutdown(dp):
    logging.warning('Shutting down..')
    await bot.delete_webhook()
    await dp.storage.close()
    await dp.storage.wait_closed()
    logging.warning('Bye!')


if __name__ == '__main__':
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )
