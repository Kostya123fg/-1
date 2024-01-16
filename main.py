 # -*- coding: utf-8 -*-
import codecs



import asyncio

from aiogram.types import InlineQuery, \
    InputTextMessageContent, InlineQueryResultArticle

from aiogram.utils.markdown import link

from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

from modules import start as start
from aiogram import Bot, Dispatcher

bot = Bot(token="6802713066:AAGVk6AfFPkbf8gjKE4aAYvMOkG4LlvWwds")
dp = Dispatcher(bot)

user_cd = "user/"
film_cd = 'films/films.txt'
channels_cd = 'channels/channels.txt'
id_cd = 'id/id.txt'


adm_id = '738799040'

async def reg(a,b):
    try:
        try:
            with codecs.open(str(user_cd) + str(a) +".txt", 'r' ,encoding="UTF-8") as file:
                file.close()

        except:

            with codecs.open(str(user_cd) + str(a) +  ".txt", 'w' ,encoding="UTF-8") as file:
                file.write("{'name_film': 0,'link_film': 0,'num_film': 0,'quest': 0,'link_channel': 0}")
                file.close()


            with codecs.open("all_users/all_users.txt", 'r' ,encoding="UTF-8") as file:
                q = str(file.readline())
                q = eval(q)
                file.close()

            q.append(str(a))

            with codecs.open("all_users/all_users.txt", 'w' ,encoding="UTF-8") as file:
                file.write(str(q))
                file.close()


        with codecs.open(str(user_cd) + str(a) +".txt", 'r' ,encoding="UTF-8") as file:
            user_data = str(file.readline())
            file.close()

        return eval(str(user_data))

    except Exception as ex:
        print(ex)

@dp.callback_query_handler(text='view_films')
async def view_films_callback_handler(call):
    user = await reg(a=str(call.from_user.id), b=str(call.from_user.username))

    with codecs.open(str(film_cd), 'r', encoding="UTF-8") as file:
        films_data = str(file.readline())
        films_data = eval(films_data)
        file.close()

    films_keyboard = InlineKeyboardMarkup()

    for code, film_info in films_data.items():
        film_title = film_info[1]
        button = InlineKeyboardButton(film_title, callback_data=f'view_film_{code}')
        films_keyboard.add(button)

    await bot.send_message(call.from_user.id, text="Выберите фильм:", reply_markup=films_keyboard)

@dp.callback_query_handler(lambda c: c.data.startswith('view_film_'))
async def view_film_callback_handler(call):
    film_code = call.data.split('_')[2]

    with codecs.open(str(film_cd), 'r', encoding="UTF-8") as file:
        films_data = str(file.readline())
        films_data = eval(films_data)
        file.close()

    if film_code in films_data:
        film_info = films_data[film_code]
        film_text = f"🎬 *Название фильма:* {film_info[1]}\n\n** {film_info[2]}"
        await bot.send_photo(chat_id=call.from_user.id, photo=str(film_info[0]), caption=film_text, parse_mode='Markdown')
    else:
        await bot.send_message(call.from_user.id, text="Фильм не найден.")

@dp.message_handler(commands=['admin'])
async def send_welcome(message):
    user = await reg(a=str(message.from_user.id), b=str(message.from_user.username))

    if str(adm_id) == str(message.from_user.id):
        inline_kb1 = InlineKeyboardMarkup()
        inline_btn_1 = InlineKeyboardButton('📌Сделать рассылку ', callback_data='add_send')
        inline_btn_2 = InlineKeyboardButton('📌Сделать рассылку с фотографией', callback_data='add_send_photo')
        inline_btn_3 = InlineKeyboardButton('🎥Добавить фильм', callback_data='add_film')
        inline_btn_4 = InlineKeyboardButton('📈Статистика', callback_data='stat')
        inline_btn_5 = InlineKeyboardButton('📌Удалить номер фильма', callback_data='delete_number')
        inline_btn_6 = InlineKeyboardButton('📋Просмотреть список фильмов', callback_data='view_films')
        inline_btn_exit = InlineKeyboardButton('🚪Выход', callback_data='exit_admin')

        inline_kb1.add(inline_btn_1).add(inline_btn_2).add(inline_btn_3).add(inline_btn_4).add(inline_btn_5).add(inline_btn_6)
        inline_kb1.add(inline_btn_exit)  # Add the "Exit" button

        await bot.send_message(chat_id=message.from_user.id, text='*Админ панель*', parse_mode='Markdown',
                               reply_markup=inline_kb1)
    else:

        await bot.send_message(chat_id=message.from_user.id, text='*❌ Доступ запрещен.*', parse_mode='Markdown')




@dp.callback_query_handler(text='exit_admin')
async def exit_admin_callback_handler(call):
    user = await reg(a=str(call.from_user.id), b=str(call.from_user.username))

    # Reset any admin-specific data
    # For example, you may want to clear any ongoing actions in the admin panel
    # user['some_key'] = None

    with codecs.open(str(user_cd) + str(call.from_user.id) + ".txt", 'w', encoding="UTF-8") as file:
        file.write(str(user))
        file.close()

    # Clear the chat history and send a new message without an inline keyboard
    await dp.bot.send_message(chat_id=call.from_user.id, text="🔎 Для поиска отправьте КОД фильма/сериала", parse_mode='Markdown')

    # Optional: You can also hide the keyboard here if you have any
    # await dp.bot.send_message(chat_id=call.from_user.id, text="Привет! 👋 Я - бот по поиску фильмов...", reply_markup=types.ReplyKeyboardRemove())





@dp.message_handler(content_types=['photo'])
async def handle_docs_photo(message):

    user = await reg(a = str(message.from_user.id), b = str(message.from_user.username))


    if user['quest'] == 888:

        with codecs.open("id/id.txt", 'r' ,encoding="UTF-8") as file:
            q = str(file.readline())
            q = eval(q)
            file.close()

        q = int(q) + 1

        with codecs.open("id/id.txt", 'w' ,encoding="UTF-8") as file:
            file.write(str(q))
            file.close()

        await message.photo[-1].download('photo/photo_' + str(q) + '.jpg')


        user['quest'] = 0

        with codecs.open(str(user_cd) + str(message.from_user.id) +".txt", 'w' ,encoding="UTF-8") as file:
            file.write(str(user))
            file.close()

        with codecs.open("all_users/all_users.txt", 'r' ,encoding="UTF-8") as file:
            g = str(file.readline())
            g = eval(g)
            file.close()

        for i in g:
            try:
                print(1)
                await bot.send_photo(chat_id = i,photo = open('photo/photo_' + str(q) + '.jpg','rb'),caption = str(message.caption))
            except Exception as ex:
                print(ex)

        await bot.send_message(chat_id = message.from_user.id, text = 'Рассылка прошла успешно.')


@dp.message_handler(commands = ['start'])
async def send_welcome(message):

    a = 0
    c = 0

    user = await reg(a = str(message.from_user.id), b = str(message.from_user.username))


    with codecs.open(str(channels_cd), 'r' ,encoding="UTF-8") as file:
        channels_me = str(file.readline())
        channels_me = eval(channels_me)
        file.close()


    if len(channels_me) == 0:
        c = 1
    else:
        inline_kb1 = InlineKeyboardMarkup()
        for i in channels_me:
            user_channel_status = await bot.get_chat_member(chat_id='@' + str(i), user_id= message.from_user.id)

            if user_channel_status["status"] == 'left':


                for i in channels_me:
                    inline_btn_1 = InlineKeyboardButton(str(channels_me[i]), url='https://t.me/'+ str(i))

                    inline_kb1.add(inline_btn_1)

                inline_btn_2 = InlineKeyboardButton('Поиск', callback_data='check')
                inline_kb1.add(inline_btn_2)

                await bot.send_message(chat_id = message.from_user.id, text = '*📝 Для использования бота, вы должны быть подписаны на наши каналы:*',reply_markup = inline_kb1,parse_mode = 'Markdown')
                c = 0
                break
            else:
                c = 1
    if c == 1:

       await bot.send_message(message.from_user.id, text = '*нажмите на кнопку 🔍Поиск 👇*',parse_mode = 'Markdown',reply_markup = start.greet_kb1)


@dp.callback_query_handler(text = 'stat')
async def vote_up_cb_handler(call):
    user = await reg(a = str(call.from_user.id), b = str(call.from_user.username))

    with codecs.open("all_users/all_users.txt", 'r' ,encoding="UTF-8") as file:
        q = str(file.readline())
        q = eval(q)
        file.close()

    await bot.send_message(call.from_user.id, text = '*📈Количество людей в боте: ' + str(len(q)) + '*',parse_mode = 'Markdown')

@dp.callback_query_handler(text = 'add_channel')
async def vote_up_cb_handler(call):
    user = await reg(a = str(call.from_user.id), b = str(call.from_user.username))

    user['quest'] = 200

    with codecs.open(str(user_cd) + str(call.from_user.id) +".txt", 'w' ,encoding="UTF-8") as file:
        file.write(str(user))
        file.close()

    await bot.send_message(call.from_user.id, text = '*Введите ссылку на канал без @\n\nПример: для добавления канала @twochannel, введите twochannel*',parse_mode = 'Markdown')

@dp.callback_query_handler(text = 'delete_number')
async def vote_up_cb_handler(call):
    user = await reg(a = str(call.from_user.id), b = str(call.from_user.username))

    user['quest'] = 6661

    with codecs.open(str(user_cd) + str(call.from_user.id) +".txt", 'w' ,encoding="UTF-8") as file:
        file.write(str(user))
        file.close()

    await bot.send_message(call.from_user.id, text = '*Введите номер фильма, который необходимо удалить*',parse_mode = 'Markdown')


@dp.callback_query_handler(text = 'delete_channel')
async def vote_up_cb_handler(call):
    user = await reg(a = str(call.from_user.id), b = str(call.from_user.username))

    user['quest'] = 500

    h = ''

    with codecs.open(str(user_cd) + str(call.from_user.id) +".txt", 'w' ,encoding="UTF-8") as file:
        file.write(str(user))
        file.close()

    with codecs.open(str(channels_cd), 'r' ,encoding="UTF-8") as file:
        channels_me = str(file.readline())
        channels_me = eval(channels_me)
        file.close()

    for i in channels_me:
        h = h + str(i) + '\n'

    await bot.send_message(call.from_user.id, text = '*Список ваших каналов:\n' + str(h) + '\n\nВведите одно из них, чтобы удалить.*',parse_mode = 'Markdown')



@dp.callback_query_handler(text='add_send')
async def vote_up_cb_handler(call):
    user = await reg(a=str(call.from_user.id), b=str(call.from_user.username))
    user['quest'] = 100
    with codecs.open(str(user_cd) + str(call.from_user.id) + ".txt", 'w', encoding="UTF-8") as file:
        file.write(str(user))
        file.close()
    await bot.send_message(call.from_user.id, text='*❗️Введите сообщение для рассылки*', parse_mode='Markdown')


@dp.callback_query_handler(text='add_send_photo')
async def vote_up_cb_handler(call):
    user = await reg(a=str(call.from_user.id), b=str(call.from_user.username))
    user['quest'] = 888
    with codecs.open(str(user_cd) + str(call.from_user.id) + ".txt", 'w', encoding="UTF-8") as file:
        file.write(str(user))
        file.close()
    await bot.send_message(call.from_user.id, text='*❗️Введите сообщение с фотографией для рассылки*', parse_mode='Markdown')


@dp.callback_query_handler(text='add_film')
async def vote_up_cb_handler(call):
    user = await reg(a=str(call.from_user.id), b=str(call.from_user.username))
    user['quest'] = 1
    with codecs.open(str(user_cd) + str(call.from_user.id) + ".txt", 'w', encoding="UTF-8") as file:
        file.write(str(user))
        file.close()
    await bot.send_message(call.from_user.id, text='*Введите номер, под которым будет фильм*', parse_mode='Markdown')



@dp.callback_query_handler(text = 'add_film')
async def vote_up_cb_handler(call):
    user = await reg(a = str(call.from_user.id), b = str(call.from_user.username))

    user['quest'] = 1

    with codecs.open(str(user_cd) + str(call.from_user.id) +".txt", 'w' ,encoding="UTF-8") as file:
        file.write(str(user))
        file.close()

    await bot.send_message(call.from_user.id, text = '*Введите номер, под которым будет фильм*',parse_mode = 'Markdown')


@dp.callback_query_handler(text = 'check')
async def vote_up_cb_handler(call):
    a = 0
    c = 0

    user = await reg(a = str(call.from_user.id), b = str(call.from_user.username))


    with codecs.open(str(channels_cd), 'r' ,encoding="UTF-8") as file:
        channels_me = str(file.readline())
        channels_me = eval(channels_me)
        file.close()


    if len(channels_me) == 0:
        c = 1
    else:
        inline_kb1 = InlineKeyboardMarkup()
        for i in channels_me:
            user_channel_status = await bot.get_chat_member(chat_id='@' + str(i), user_id= call.from_user.id)

            if user_channel_status["status"] == 'left':


                for i in channels_me:
                    inline_btn_1 = InlineKeyboardButton(str(channels_me[i]), url='https://t.me/'+ str(i))

                    inline_kb1.add(inline_btn_1)

                inline_btn_2 = InlineKeyboardButton('Поиск', callback_data='check')
                inline_kb1.add(inline_btn_2)
                await bot.send_message(chat_id = call.from_user.id, text = '*📝 Для использования бота, вы должны быть подписаны на наши каналы:*',reply_markup = inline_kb1,parse_mode = 'Markdown')
                c = 0
                break
            else:
                c = 1
    if c == 1:

       await bot.send_message(call.from_user.id, text = '*Привет это 🍿КИНОМОЛОКО - БОТ | Поиск🔍\nЧтобы узнать название фильмов из ЮТУБ | ТИК ТОК вам нужно ввести код фильма.\nНажмите на «🔎Поиск» 👇*',parse_mode = 'Markdown',reply_markup = start.greet_kb1)


@dp.message_handler()
async def send_welcome(message):
    a = 0
    c = 0
    user = await reg(a = str(message.from_user.id), b = str(message.from_user.username))


    with codecs.open(str(channels_cd), 'r' ,encoding="UTF-8") as file:
        channels_me = str(file.readline())
        channels_me = eval(channels_me)
        file.close()


    if len(channels_me) == 0:
        c = 1
    else:
        inline_kb1 = InlineKeyboardMarkup()
        for i in channels_me:
            user_channel_status = await bot.get_chat_member(chat_id='@' + str(i), user_id= message.from_user.id)
            if user_channel_status["status"] == 'left':


                for i in channels_me:

                    inline_btn_1 = InlineKeyboardButton(str(channels_me[i]), url='https://t.me/'+ str(i))

                    inline_kb1.add(inline_btn_1)

                inline_btn_2 = InlineKeyboardButton('Поиск', callback_data='check')
                inline_kb1.add(inline_btn_2)
                await bot.send_message(chat_id = message.from_user.id, text = '*📝 Для использования бота, вы должны быть подписаны на наши каналы:*',reply_markup = inline_kb1,parse_mode = 'Markdown')
                c = 0
                break
            else:
                c = 1
    if c == 1:

        if str(message.text) == '🔎Поиск':
            a = 1
            await bot.send_message(chat_id = message.from_user.id,text = '*🔎 Для поиска отправьте КОД фильма/сериала*',parse_mode = 'Markdown')
        if user['quest'] == 1 and a == 0:
            a = 1

            with codecs.open(str(film_cd), 'r' ,encoding="UTF-8") as file:
                q = str(file.readline())
                q = eval(q)
                file.close()


            if str(message.text) in q:


                user['quest'] = 0

                with codecs.open(str(user_cd) + str(message.from_user.id) +".txt", 'w' ,encoding="UTF-8") as file:
                    file.write(str(user))
                    file.close()

                await bot.send_message(chat_id = message.from_user.id, text = '*Данный номер уже существует! Попробуйте ещё раз.*',parse_mode = 'Markdown')

            else:


                user['quest'] = 3
                user['num_film'] = str(message.text)


                with codecs.open(str(user_cd) + str(message.from_user.id) +".txt", 'w' ,encoding="UTF-8") as file:
                    file.write(str(user))
                    file.close()


                await bot.send_message(chat_id = message.from_user.id, text = '*Название фильма:*',parse_mode = 'Markdown')

        if user['quest'] == 3 and a == 0:
            a = 1

            user['link_film'] = str(message.text)
            user['quest'] = 992

            with codecs.open(str(user_cd) + str(message.from_user.id) + ".txt", 'w', encoding="UTF-8") as file:
                file.write(str(user))
                file.close()

            await bot.send_message(chat_id=message.from_user.id, text='*Введите информацию о фильме*',
                                   parse_mode='Markdown')

        if user['quest'] == 992 and a == 0:
            a = 1
            user['info_film'] = str(message.text)
            user['quest'] = 993

            with codecs.open(str(user_cd) + str(message.from_user.id) + ".txt", 'w', encoding="UTF-8") as file:
                file.write(str(user))
                file.close()

            await bot.send_message(chat_id=message.from_user.id, text='*Введите ссылку на фотографию для фильма*',
                                   parse_mode='Markdown')

        if user['quest'] == 993 and a == 0:
            a = 1
            with codecs.open(str(film_cd), 'r', encoding="UTF-8") as file:
                q = str(file.readline())
                q = eval(q)
                file.close()

            q[str(user['num_film'])] = [str(message.text), str(user['link_film']), str(user['info_film'])]

            with codecs.open(str(film_cd), 'w', encoding="UTF-8") as file:
                file.write(str(q))
                file.close()

            user['quest'] = 0

            with codecs.open(str(user_cd) + str(message.from_user.id) + ".txt", 'w', encoding="UTF-8") as file:
                file.write(str(user))
                file.close()

            await bot.send_message(chat_id=message.from_user.id, text='*Фильм успешно добавлен!*',
                                   parse_mode='Markdown')
        if user['quest'] == 100 and a == 0:
            a = 1

            user['quest'] = 0

            with codecs.open(str(user_cd) + str(message.from_user.id) +".txt", 'w' ,encoding="UTF-8") as file:
                file.write(str(user))
                file.close()

            with codecs.open("all_users/all_users.txt", 'r' ,encoding="UTF-8") as file:
                q = str(file.readline())
                q = eval(q)
                file.close()

            for i in q:
                try:
                    await bot.send_message(chat_id = i, text = str(message.text))
                except:
                    pass


            await bot.send_message(chat_id = message.from_user.id, text = '*Рассылка прошла успешно.*',parse_mode = 'Markdown')


        if user['quest'] == 200 and a == 0:
            a = 1

            user['link_channel'] = str(message.text)

            user['quest'] = 300

            with codecs.open(str(user_cd) + str(message.from_user.id) +".txt", 'w' ,encoding="UTF-8") as file:
                file.write(str(user))
                file.close()


            await bot.send_message(chat_id = message.from_user.id, text = '*Хорошо. Теперь укажите название канала*',parse_mode = 'Markdown')

        if user['quest'] == 300 and a == 0:
            a = 1


            user['quest'] = 0

            with codecs.open(str(user_cd) + str(message.from_user.id) +".txt", 'w' ,encoding="UTF-8") as file:
                file.write(str(user))
                file.close()


            with codecs.open(str(channels_cd), 'r' ,encoding="UTF-8") as file:
                channels_me = str(file.readline())
                channels_me = eval(channels_me)
                file.close()


            channels_me[str(user['link_channel'])] = str(message.text)

            with codecs.open(str(channels_cd), 'w' ,encoding="UTF-8") as file:
                file.write(str(channels_me))
                file.close()

            await bot.send_message(chat_id = message.from_user.id, text = '*Канал успешно добавлен!*',parse_mode = 'Markdown')


        if user['quest'] == 6661 and a == 0:
            a = 1

            user['quest'] = 0

            with codecs.open(str(user_cd) + str(message.from_user.id) +".txt", 'w' ,encoding="UTF-8") as file:
                file.write(str(user))
                file.close()


            with codecs.open(str(film_cd), 'r' ,encoding="UTF-8") as file:
                q = str(file.readline())
                q = eval(q)
                file.close()


            if str(message.text) in q:
                del q[str(message.text)]

                with codecs.open(str(film_cd), 'w' ,encoding="UTF-8") as file:
                    file.write(str(q))
                    file.close()

                await message.reply('Номер успешно удалён')

            else:
                await message.reply('Данный номер отсутствует')


        if user['quest'] == 500 and a == 0:
            a = 1


            user['quest'] = 0

            with codecs.open(str(user_cd) + str(message.from_user.id) +".txt", 'w' ,encoding="UTF-8") as file:
                file.write(str(user))
                file.close()


            with codecs.open(str(channels_cd), 'r' ,encoding="UTF-8") as file:
                channels_me = str(file.readline())
                channels_me = eval(channels_me)
                file.close()

            if str(message.text) in channels_me:
                del channels_me[str(message.text)]

                with codecs.open(str(channels_cd), 'w' ,encoding="UTF-8") as file:
                    file.write(str(channels_me))
                    file.close()

                await bot.send_message(chat_id = message.from_user.id,text ='*Канал успешно удалён из списка!*',parse_mode = 'Markdown')

            else:

                await bot.send_message(chat_id = message.from_user.id,text ='*Убедитесь в правильности написания канала!*',parse_mode = 'Markdown')

        if a == 0:
            a = 1
            try:
                code = int(message.text)
            except ValueError:
                await bot.send_message(chat_id=message.from_user.id,
                                       text='*Ошибка: Некорректный код. Пожалуйста, введите корректный код в виде числа.*',
                                       parse_mode='Markdown')
                return

            with codecs.open(str(film_cd), 'r', encoding="UTF-8") as file:
                q = str(file.readline())
                q = eval(q)
                file.close()
            if str(code) in q:
                try:
                    film_info = f"🎬 *Название фильма:* {q[str(code)][1]}\n\n** {q[str(code)][2]}"
                    await bot.send_photo(chat_id=message.from_user.id, photo=str(q[str(code)][0]),
                                         caption=film_info, parse_mode='Markdown')
                except Exception as ex:
                    print(ex)
            else:
                await bot.send_message(chat_id=message.from_user.id,
                                       text='*Ошибка: Код не найден. Пожалуйста, введите корректный код.*',
                                       parse_mode='Markdown')

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(dp.start_polling())







