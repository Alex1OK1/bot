import logging
from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CommandHandler, CallbackQueryHandler
from telegram import ReplyKeyboardMarkup
from telegram.ext import ConversationHandler
import sqlite3
from random import randint, sample, choice, shuffle
from main import start_markup
from gtts import gTTS
stop_keyboard = [['/stop']]
stop_markup = ReplyKeyboardMarkup(stop_keyboard, one_time_keyboard=True)
da_net = [['Да', 'Нет']]
da_net_markup = ReplyKeyboardMarkup(da_net, one_time_keyboard=True)

win_stickers = ["CAACAgIAAxkBAAEEroBieAOdhgs-63vqO-d5o7I_P5Sz7gACbRQAAvh48Ev_35tLbqKxRyQE",
                "CAACAgIAAxkBAAEEroRieAVyHEGctGEtQkpc4NRMqsbgHgAC6yMAAj_lAUl35ZIodwxRkyQE",
                "CAACAgIAAxkBAAEEropieAWENVIGRWl9FxSZ60kJGWh3yAACUBIAAmiK-UusK61yxrWHkyQE",
                "CAACAgIAAxkBAAEEroxieAWGPIt0d8HJ2thZL8um0yrfsgACShcAAnq68EsNzlcoSPmYyyQE",
                "CAACAgIAAxkBAAEErpBieAYI3GRqblYOW79n54OltYe7nQACDhsAApwiuEkaScQf14vkKyQE",
                "CAACAgIAAxkBAAEErpJieAYOLlTMD8eEek4pN3mALtHfEQAC4RUAArRM2EnZ3DPB3rAICCQE"]
lose_stickers = ["CAACAgIAAxkBAAEEroZieAV7k0CAKbzo3feMb5P5mmtxhQACgxAAAmuA8UvdlI_YEKj09yQE",
                 "CAACAgIAAxkBAAEErohieAWAW8NFVMDoPFYravCidPgN2wACcBIAAt6p8Et8ICHIsOd3qyQE",
                 "CAACAgIAAxkBAAEEro5ieAWPM_NAbkQxQXzXKMQCJ2vBQQACmRUAAit1eEh1yI6rouJTiSQE"]

connect_words = sqlite3.connect("words.db", check_same_thread=False)
cursor_words = connect_words.cursor()

id = 0
z = []
hint_list = []
user_id = -1


def words(update, context):
    global z, id, user_id
    user_id = cursor_words.execute(
        "SELECT id FROM users WHERE name = '" + update.message.from_user.username + "'").fetchall()[0][0]
    connect_words.commit()
    update.message.reply_text("Чтобы остановить игру напиши команду /stop", reply_markup=stop_markup)
    z = cursor_words.execute("SELECT * FROM words").fetchall()
    connect_words.commit()
    id = randint(0, len(z) - 1)
    update.message.reply_text("Переведите слово(перевод должен быть в несовершенном виде инфинитива)\n" + z[id][1])
    return 1


def stop(update, context):
    update.message.reply_text("Хароооооош!", reply_markup=start_markup)
    return ConversationHandler.END


def question(update, context):
    global z, id
    v = update.message.text
    print(z[id])
    if v.lower() == z[id][2]:
        update.message.reply_text(
            "Абсолютно верно 👍, ваши баллы были начислены вам на счет. ",
            reply_markup=da_net_markup)
        update.message.reply_sticker(choice(win_stickers))
        update.message.reply_text("Хотите прослушать как читается это слово? (Да,Нет)")
        print(user_id)
        print(cursor_words.execute("UPDATE users SET score = score + ? WHERE id = ?", (10, user_id)).fetchall())
        connect_words.commit()
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
    if v.lower() == z[id][2]:
        update.message.reply_text(
            "Абсолютно верно 👍, ваши баллы были начислены вам на счет. ",
            reply_markup=da_net_markup)
        update.message.reply_sticker(choice(win_stickers))
        update.message.reply_text("Хотите прослушать как читается это слово? (Да,Нет)")
        print(cursor_words.execute("UPDATE users SET score = score + ? WHERE id = ?", (5, user_id)).fetchall())
        connect_words.commit()
        return 6
    else:
        update.message.reply_text("Ответ не верный😞(((", reply_markup=da_net_markup)
        update.message.reply_text("Правильный ответ: " + z[id][2])
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
        hint_list = [z[id][2]] + sample(z, 2)
        hint_list[1] = hint_list[1][2]
        hint_list[2] = hint_list[2][2]
        while len(set(hint_list)) != 3:
            hint_list = list(set(hint_list))
            hint_list.append(choice(z)[2])
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
        update.message.reply_text("Переведите слово(перевод должен быть в несовершенном виде инфинитива)\n" + z[id][1])
        return 1


def wanttolisten(update, context):
    global z, id
    v = update.message.text
    if v.lower() in "да":
        word = gTTS(text=z[id][1], lang="en", slow=False)
        word.save("currentword.mp3")
        update.message.reply_audio(open(r'currentword.mp3', 'rb'))
        update.message.reply_text("Хотите продолжить игру?", reply_markup=da_net_markup)
    elif v.lower() in "нет":
        update.message.reply_text("Хотите продолжить игру?", reply_markup=da_net_markup)
    return 4


conv_handler = ConversationHandler(
    entry_points=[CommandHandler('words', words)],
    states={
        1: [MessageHandler(Filters.text & ~Filters.command, question)],
        2: [MessageHandler(Filters.text & ~Filters.command, hint)],
        3: [MessageHandler(Filters.text & ~Filters.command, words)],
        4: [MessageHandler(Filters.text & ~Filters.command, continueornot)],
        5: [MessageHandler(Filters.text & ~Filters.command, hintornot)],
        6: [MessageHandler(Filters.text & ~Filters.command, wanttolisten)]
    },

    fallbacks=[CommandHandler('stop', stop)]
)
