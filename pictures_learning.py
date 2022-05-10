import logging
from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CommandHandler, CallbackQueryHandler
from telegram import ReplyKeyboardMarkup
from telegram.ext import ConversationHandler
from random import randint, sample, choice, shuffle
from main import start_markup
import sqlite3
from gtts import gTTS

import os

all_pics = os.listdir("C:\\Users\\Alex4\\PycharmProjects\\bot\\pictures")
z = [i[:-4] for i in all_pics]
id = 0
user_id = -1
connect_points = sqlite3.connect("words.db", check_same_thread=False)
cursor_points = connect_points.cursor()
stop_keyboard = [['/stop']]
stop_markup = ReplyKeyboardMarkup(stop_keyboard, one_time_keyboard=True)
da_net = [['Да', 'Нет']]
da_net_markup = ReplyKeyboardMarkup(da_net, one_time_keyboard=True)
hint_list = []
win_stickers = ["CAACAgIAAxkBAAEEroBieAOdhgs-63vqO-d5o7I_P5Sz7gACbRQAAvh48Ev_35tLbqKxRyQE",
                "CAACAgIAAxkBAAEEroRieAVyHEGctGEtQkpc4NRMqsbgHgAC6yMAAj_lAUl35ZIodwxRkyQE",
                "CAACAgIAAxkBAAEEropieAWENVIGRWl9FxSZ60kJGWh3yAACUBIAAmiK-UusK61yxrWHkyQE",
                "CAACAgIAAxkBAAEEroxieAWGPIt0d8HJ2thZL8um0yrfsgACShcAAnq68EsNzlcoSPmYyyQE",
                "CAACAgIAAxkBAAEErpBieAYI3GRqblYOW79n54OltYe7nQACDhsAApwiuEkaScQf14vkKyQE",
                "CAACAgIAAxkBAAEErpJieAYOLlTMD8eEek4pN3mALtHfEQAC4RUAArRM2EnZ3DPB3rAICCQE"]
lose_stickers = ["CAACAgIAAxkBAAEEroZieAV7k0CAKbzo3feMb5P5mmtxhQACgxAAAmuA8UvdlI_YEKj09yQE",
                 "CAACAgIAAxkBAAEErohieAWAW8NFVMDoPFYravCidPgN2wACcBIAAt6p8Et8ICHIsOd3qyQE",
                 "CAACAgIAAxkBAAEEro5ieAWPM_NAbkQxQXzXKMQCJ2vBQQACmRUAAit1eEh1yI6rouJTiSQE"]


def pics(update, context):
    global z, id, user_id
    user_id = cursor_points.execute(
        "SELECT id FROM users WHERE name = '" + update.message.from_user.username + "'").fetchall()[0][0]
    connect_points.commit()
    update.message.reply_text("Чтобы остановить игру напиши команду /stop", reply_markup=stop_markup)
    id = randint(0, len(z) - 1)
    update.message.reply_text("Напишите слово изображенное на картинке на английском языке")
    update.message.reply_photo(open("C:\\Users\\Alex4\\PycharmProjects\\bot\\pictures\\" + z[id] + '.jpg', 'rb'))
    return 1


def stop(update, context):
    update.message.reply_text("Хароооооош!", reply_markup=start_markup)
    return ConversationHandler.END


def question(update, context):
    global z, id
    v = update.message.text
    print(z[id])
    if v.lower() == z[id]:
        update.message.reply_text(
            "Абсолютно верно 👍, ваши баллы были начислены вам на счет. ",
            reply_markup=da_net_markup)
        update.message.reply_sticker(choice(win_stickers))
        update.message.reply_text("Хотите прослушать как читается это слово? (Да,Нет)")
        print(user_id)
        print(cursor_points.execute("UPDATE users SET score = score + ? WHERE id = ?", (10, user_id)).fetchall())
        connect_points.commit()
        return 6
    else:
        update.message.reply_text("Ответ не верный😞(((",
                                  reply_markup=da_net_markup)
        update.message.reply_sticker(choice(lose_stickers))
        update.message.reply_text("Хотите воспользоваться подсказкой? (Да,Нет)")
        return 5


def hint(update, context):
    global z, id
    v = update.message.text
    print(z[id])
    if v.lower() == z[id]:
        update.message.reply_text(
            "Абсолютно верно 👍, ваши баллы были начислены вам на счет. ",
            reply_markup=da_net_markup)
        update.message.reply_sticker(choice(win_stickers))
        update.message.reply_text("Хотите прослушать как читается это слово? (Да,Нет)")
        print(cursor_points.execute("UPDATE users SET score = score + ? WHERE id = ?", (5, user_id)).fetchall())
        connect_points.commit()
        return 6
    else:
        update.message.reply_text("Ответ не верный😞(((", reply_markup=da_net_markup)
        update.message.reply_text("Правильный ответ: " + z[id])
        update.message.reply_sticker(choice(lose_stickers))
        update.message.reply_text("Хотите прослушать как читается это слово? (Да,Нет)")
        return 6


def hintornot(update, context):
    global z, id, hint_list
    v = update.message.text
    if v.lower() in "нет":
        update.message.reply_text("Хотите продолжить игру?", reply_markup=da_net_markup)
        return 4
    elif v.lower() in "да":
        hint_list = [z[id]] + sample(z, 2)
        while len(set(hint_list)) != 3:
            hint_list = list(set(hint_list))
            hint_list.append(choice(z))
        shuffle(hint_list)
        update.message.reply_text("Выберите 1 слово",
                                  reply_markup=ReplyKeyboardMarkup([hint_list], one_time_keyboard=True))
        return 2


def continueornot(update, context):
    global z, id
    v = update.message.text
    if v.lower() in "нет":
        update.message.reply_text("GG WP", reply_markup=start_markup)
        update.message.reply_sticker("CAACAgIAAxkBAAEErpRieAcjAAEaF8getDqoPMV7nNMdfZ4AAhwRAAJcxFFJV96Mu-GSkgUkBA")

        return ConversationHandler.END
    elif v.lower() in "да":
        update.message.reply_text("OKAAAAAY, Let's GO", reply_markup=stop_markup)
        id = randint(0, len(z) - 1)
        update.message.reply_text("Напишите слово изображенное на картинке на английском языке")
        update.message.reply_photo(open("C:\\Users\\Alex4\\PycharmProjects\\bot\\pictures\\" + z[id] + '.jpg', 'rb'))
        return 1


def wanttolisten(update, context):
    global z, id
    v = update.message.text
    if v.lower() in "да":
        word = gTTS(text=z[id], lang="en", slow=False)
        word.save("currentword.mp3")
        update.message.reply_audio(open(r'currentword.mp3', 'rb'))
        update.message.reply_text("Хотите продолжить игру?", reply_markup=da_net_markup)
    elif v.lower() in "нет":
        update.message.reply_text("Хотите продолжить игру?", reply_markup=da_net_markup)
    return 4


conv_handler = ConversationHandler(
    entry_points=[CommandHandler('pictures', pics)],
    states={
        1: [MessageHandler(Filters.text & ~Filters.command, question)],
        2: [MessageHandler(Filters.text & ~Filters.command, hint)],
        3: [MessageHandler(Filters.text & ~Filters.command, pics)],
        4: [MessageHandler(Filters.text & ~Filters.command, continueornot)],
        5: [MessageHandler(Filters.text & ~Filters.command, hintornot)],
        6: [MessageHandler(Filters.text & ~Filters.command, wanttolisten)]
    },

    fallbacks=[CommandHandler('stop', stop)]
)
