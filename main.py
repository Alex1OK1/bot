import logging
from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CommandHandler
from telegram import ReplyKeyboardMarkup

import sqlite3

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)
start_keyboard = [['/words', '/pictures'],
                  ['/top', '/start']]
start_markup = ReplyKeyboardMarkup(start_keyboard, one_time_keyboard=True)
logger = logging.getLogger(__name__)

TOKEN = '5370722364:AAHiDt3uZT1QXYwK56NrGMYjbF1qf8Wgtuc'

connect_users = sqlite3.connect("words.db", check_same_thread=False)
cursor_users = connect_users.cursor()
users = cursor_users.execute("SELECT * FROM users").fetchall()
id_of_newloh = 0
try:
    id_of_newloh = users[-1][0]
except:
    id_of_newloh = 0
connect_users.commit()
import words_learning
import pictures_learning

def start(update, context):
    global users, id_of_newloh
    print("QQQQQQQQQQQQQQQQQQQQQQQQ",any(update.message.from_user.username in i for i in users))
    update.message.reply_text(
        "Привет, " + update.message.from_user[
            'first_name'] + ", Я Ботяра.\nЯ обучу тебя английскому.\nДля начала выбери режим.",
        reply_markup=start_markup)
    if not any(update.message.from_user.username in i for i in users):
        users.append((id_of_newloh + 1, update.message.from_user.username))
        cursor_users.execute(
            f"INSERT INTO users VALUES({id_of_newloh + 1}, '{update.message.from_user.username}',0 ) ").fetchall()
        connect_users.commit()
        id_of_newloh += 1


def help(update, context):
    update.message.reply_text(
        "Вы можете выбрать 2 режима:\nОтгадывание слова по картинке или перевод слова с английского на русский.\n"
        "Также вы можете взять подсказку, чтобы получить 3 варианта ответа.\n"
        "В боте есть свой рейтинг. За каждое правильноотгаданное слово вы получаетте баллы.\nПри использовании подсказки баллы уменьшаются вдвое\n"
        "Чтобы узнать топ пользователей введите команду /top")


def top(update, context):
    ret = ""
    top_scores = cursor_users.execute("SELECT name, score FROM users ORDER BY score DESC LIMIT 10").fetchall()
    print(top_scores)
    for i, aboba in enumerate(top_scores):
        ret += str(i+1) + " @" + str(aboba[0]) + " " + str(aboba[1]) + "\n"
    update.message.reply_text(ret)


def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("top", top))
    dp.add_handler(words_learning.conv_handler)
    dp.add_handler(pictures_learning.conv_handler)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
