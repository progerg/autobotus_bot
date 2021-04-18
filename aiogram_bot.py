import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.helper import Helper, HelperMode, ListItem
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

API_TOKEN = 'token'  # !!!!!!!!!!!!TEST BOT

msg = MIMEMultipart()
msg['From'] = "mail"
msg['To'] = "mail"

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())

CHECK_LIST = ['Забыли вещь 🧳', 'Проверка грамотности 💡', 'Частые вопросы ❓', 'Жалобы / предложения 😡',
              'Транспорт онлайн 🚌']


class TestStates(Helper):
    mode = HelperMode.snake_case

    MAIN_MENU = ListItem()
    COMPLAINT_IN_BOT = ListItem()
    BUS_NUMBER = ListItem()
    LOST_THING = ListItem()
    TEST_STATE_4 = ListItem()
    TEST_STATE_5 = ListItem()


@dp.message_handler(commands='start', state=TestStates.MAIN_MENU)
@dp.message_handler(commands='start')
async def start_cmd_handler(message: types.Message):
    keyboard_markup = types.ReplyKeyboardMarkup(row_width=3)
    # default row_width is 3, so here we can omit it actually
    # kept for clearness

    text_and_data_1 = (
        ('Забыли вещь 🧳', '/lost'),
        ('Проверка грамотности 💡', '/test'),
        ('Частые вопросы ❓', '/questions'),
    )
    text_and_data_2 = (('Жалобы / предложения 😡', '/complaints'),
                       ('Транспорт онлайн 🚌', '/transport'),)
    # in real life for the callback_data the callback data factory should be used
    # here the raw string is used for the simplicity
    row_btns_1 = (types.KeyboardButton(text, callback_data=data) for text, data in text_and_data_1)

    keyboard_markup.row(*row_btns_1)
    row_btns_2 = (types.KeyboardButton(text, callback_data=data) for text, data in text_and_data_2)
    keyboard_markup.row(*row_btns_2)

    START_MESSAGE = '''Привет пользователь общественного транспорта нашего города! 🤟
Я, чат-бот «Автоботус», онлайн консультант о транспорте Воронежа. Здесь всегда актуально об общественном транспорте города!

На данным момент я умею:
🔸Отвечать на частые вопросы
🔹Отправлять жалобы и предложения
🔸Проводить тест на твои знания о правильном использовании общественного транспорта
🔹Если ты забыл вещь, то обращайся ко мне
🔸Транспорт онлайн на карте города

Я очень простой бот, надеюсь, ты во мне разберёшься. А если нет, то пиши нашей технической поддержке — @autobotus_info'''
    state = dp.current_state(user=message.from_user.id)
    await state.set_state(TestStates.all()[3])
    await message.reply(START_MESSAGE, reply_markup=keyboard_markup)


@dp.message_handler(state=TestStates.MAIN_MENU)
async def all_handlers(message: types.Message):
    button_text = message.text
    logger.debug('The answer is %r', button_text)

    if button_text == 'Жалобы / предложения 😡':
        keyboard_markup = types.InlineKeyboardMarkup(row_width=3)
        # default row_width is 3, so here we can omit it actually
        # kept for clearness

        text_and_data_1 = (
            ('10А', '10А'),
            ('16В', '16В'),
            ('20', '20'),
            ('20Б', '20Б'),
            ('37', '37'),
        )
        text_and_data_2 = (('50', '50'),
                           ('52АВ', '52АВ'),
                           ('54', '54'),
                           ('59АС', '59АС'),
                           ('91', '91'),
                           ('120', '120'),)
        # in real life for the callback_data the callback data factory should be used
        # here the raw string is used for the simplicity
        row_btns_1 = (types.InlineKeyboardButton(text, callback_data=data) for text, data in text_and_data_1)

        keyboard_markup.row(*row_btns_1)
        row_btns_2 = (types.InlineKeyboardButton(text, callback_data=data) for text, data in text_and_data_2)
        keyboard_markup.row(*row_btns_2)
        # in real life for the callback_data the callback data factory should be used
        # here the raw string is used for the simplicity
        message_ = 'Выберите номер автобуса'

        await message.reply(message_, reply_markup=keyboard_markup)

    if button_text == 'Забыли вещь 🧳':
        keyboard_markup = types.InlineKeyboardMarkup(row_width=3)
        # default row_width is 3, so here we can omit it actually
        # kept for clearness

        text_and_data_1 = (
            ('10А', '10А'),
            ('16В', '16В'),
            ('20', '20'),
            ('20Б', '20Б'),
            ('37', '37'),
        )
        text_and_data_2 = (('50', '50'),
                           ('52АВ', '52АВ'),
                           ('54', '54'),
                           ('59АС', '59АС'),
                           ('91', '91'),
                           ('120', '120'),)
        # in real life for the callback_data the callback data factory should be used
        # here the raw string is used for the simplicity
        row_btns_1 = (types.InlineKeyboardButton(text, callback_data=data) for text, data in text_and_data_1)

        keyboard_markup.row(*row_btns_1)
        row_btns_2 = (types.InlineKeyboardButton(text, callback_data=data) for text, data in text_and_data_2)
        keyboard_markup.row(*row_btns_2)
        # in real life for the callback_data the callback data factory should be used
        # here the raw string is used for the simplicity
        message_ = 'В каком маршруте Вы забыли вещь?'
        state = dp.current_state(user=message.from_user.id)
        await state.set_state(TestStates.all()[2])
        await message.reply(message_, reply_markup=keyboard_markup)

    if button_text == 'Частые вопросы ❓':
        keyboard_markup = types.InlineKeyboardMarkup(row_width=1)
        # default row_width is 3, so here we can omit it actually
        # kept for clearness
        text_and_data_1 = (
            ('1', '/question1'),
            ('2', '/question2'),
            ('3', '/question3'),
            ('4', '/question4'),
            ('5', '/question5')
        )
        row_btns_1 = (types.InlineKeyboardButton(text, callback_data=data) for text, data in text_and_data_1)
        keyboard_markup.row(*row_btns_1)
        # in real life for the callback_data the callback data factory should be used
        # here the raw string is used for the simplicity
        message_ = '''Выберите интересующий вопрос:
1️⃣ Какая стоимость проезда?
2️⃣ Почему нужно носить маску в общественном транспорте?
3️⃣ Когда в Воронеже заменят «маршрутки» на автобусы?
4️⃣ Как пожаловаться на работу водителя/автобуса или предложить идею?
5️⃣ Зачем нужны выделенные полосы для общественного транспорта?'''

        await message.reply(message_, reply_markup=keyboard_markup)

    if button_text == 'Проверка грамотности 💡':
        keyboard_markup = types.InlineKeyboardMarkup(row_width=3)
        keyboard_markup.add(
            types.InlineKeyboardButton('Пройти тест',
                                       url='https://vk.com/app7385430#forms/40243'),
        )

        message_ = 'Проверить свои знания в области использования общественного транспорта — легко! Просто пройдите \
наш опрос:'
        await message.reply(message_, reply_markup=keyboard_markup, )

    if button_text == 'Транспорт онлайн 🚌':
        keyboard_markup = types.InlineKeyboardMarkup(row_width=3)
        keyboard_markup.add(
            types.InlineKeyboardButton('Яндекс.Карты',
                                       url='https://yandex.ru/maps/193/voronezh/?ll=39.251930%2C51.667816&z=12'),
            types.InlineKeyboardButton('2ГИС',
                                       url='https://2gis.ru/voronezh'),
            types.InlineKeyboardButton('BusTime',
                                       url='https://www.bustime.ru/voronezh/'),
            types.InlineKeyboardButton('VrnBus',
                                       url='https://vrnbus.herokuapp.com/'),
        )

        message_ = 'Этот сервис очень хорошо разработан нашими коллегами. Движение \
общественного транспорта в режиме реального времени можно посмотреть в приложениях. \
Они также доступны на Android и на iOS ✌🏻'
        await message.reply(message_, reply_markup=keyboard_markup, )


@dp.callback_query_handler(text='/question1', state=TestStates.MAIN_MENU)
@dp.callback_query_handler(text='/question2', state=TestStates.MAIN_MENU)
@dp.callback_query_handler(text='/question3', state=TestStates.MAIN_MENU)
@dp.callback_query_handler(text='/question4', state=TestStates.MAIN_MENU)
@dp.callback_query_handler(text='/question5', state=TestStates.MAIN_MENU)
async def complaint(query: types.CallbackQuery):
    answer_data = query.data
    # always answer callback queries, even if you have nothing to say
    if answer_data == '/question1':
        text = '''1️⃣ Безналичная оплата — 21 руб.\nНаличная оплата — 23 руб.'''
    if answer_data == '/question2':
        text = '2️⃣ Масочный режим в общественном транспорте и публичных местах в \
Воронежской области ввели 12 мая 2020 года. Нарушителям грозит административная ответственность \
по ст. 20.6.1 КоАП РФ. Штраф составляет от 1 тыс. до 30 тыс. рублей.'
    if answer_data == '/question3':
        text = '3️⃣ В нашем городе идёт активная закупка автобусов на маршруты. \
Поэтому советуем подписаться на нашу новостную рассылку!'
    if answer_data == '/question4':
        text = '4️⃣ В нашем чат-боте есть функция «Жалобы/предложения». Вы выбираете свой маршрут, наш бот присылает вам \
контактную информацию перевозчика. А также мы сможем вам помочь отправить обращение на электронную почту 😉'
    if answer_data == '/question5':
        text = '5️⃣ «Выделенные полосы значительно увеличивают провозную способность улиц. Автобусы перестанут настолько \
зависеть от пробок и будут перевозить наибольшее количество горожан за наименьшее время», — рассказал мэр города\
 Вадим Кстенин.'
    await bot.send_message(query.from_user.id, text)


# Use multiple registrators. Handler will execute when one of the filters is OK
@dp.callback_query_handler(text='10А', state=TestStates.MAIN_MENU)
@dp.callback_query_handler(text='16В', state=TestStates.MAIN_MENU)
@dp.callback_query_handler(text='20', state=TestStates.MAIN_MENU)
@dp.callback_query_handler(text='20Б', state=TestStates.MAIN_MENU)
@dp.callback_query_handler(text='37', state=TestStates.MAIN_MENU)
@dp.callback_query_handler(text='50', state=TestStates.MAIN_MENU)
@dp.callback_query_handler(text='52АВ', state=TestStates.MAIN_MENU)
@dp.callback_query_handler(text='54', state=TestStates.MAIN_MENU)
@dp.callback_query_handler(text='59АС', state=TestStates.MAIN_MENU)
@dp.callback_query_handler(text='91', state=TestStates.MAIN_MENU)
@dp.callback_query_handler(text='120', state=TestStates.MAIN_MENU)
async def choose_bus(query: types.CallbackQuery):
    answer_data = query.data
    # always answer callback queries, even if you have nothing to say
    await query.answer(f'Вы выбрали {answer_data!r}')
    text = 'Если у Вас во время пользования произошли какие-то недоразумения или у вас появились идеи для перевозчика. \
То Вы можете самостоятельно обратиться в компанию (нажмите «Контакты») или мы отправим за Вас сообщение на почту \
перевозчика (нажмите «Отправка»)🚌'
    keyboard_markup = types.InlineKeyboardMarkup(row_width=3)
    # default row_width is 3, so here we can omit it actually
    # kept for clearness
    text_and_data_1 = (
        ('Отправка', '/complaint_in_bot'),
        ('Контакты', '/complaint_other')
    )
    row_btns_1 = (types.InlineKeyboardButton(text, callback_data=data) for text, data in text_and_data_1)

    keyboard_markup.row(*row_btns_1)

    await bot.send_message(query.from_user.id, text, reply_markup=keyboard_markup)


@dp.callback_query_handler(text='10А', state=TestStates.LOST_THING)
@dp.callback_query_handler(text='16В', state=TestStates.LOST_THING)
@dp.callback_query_handler(text='20', state=TestStates.LOST_THING)
@dp.callback_query_handler(text='20Б', state=TestStates.LOST_THING)
@dp.callback_query_handler(text='37', state=TestStates.LOST_THING)
@dp.callback_query_handler(text='50', state=TestStates.LOST_THING)
@dp.callback_query_handler(text='52АВ', state=TestStates.LOST_THING)
@dp.callback_query_handler(text='54', state=TestStates.LOST_THING)
@dp.callback_query_handler(text='59АС', state=TestStates.LOST_THING)
@dp.callback_query_handler(text='91', state=TestStates.LOST_THING)
@dp.callback_query_handler(text='120', state=TestStates.LOST_THING)
async def choose_bus(query: types.CallbackQuery):
    answer_data = query.data
    # always answer callback queries, even if you have nothing to say
    await query.answer(f'Вы выбрали {answer_data!r}')
    text = 'Вы можете самостоятельно обратиться в компанию (нажмите «Контакты») или мы отправим \
за Вас сообщение на почту перевозчика (нажмите «Отправка») 🧳'
    keyboard_markup = types.InlineKeyboardMarkup(row_width=3)
    # default row_width is 3, so here we can omit it actually
    # kept for clearness
    text_and_data_1 = (
        ('Отправка', '/complaint_in_bot'),
        ('Контакты', '/complaint_other')
    )
    row_btns_1 = (types.InlineKeyboardButton(text, callback_data=data) for text, data in text_and_data_1)

    keyboard_markup.row(*row_btns_1)

    await bot.send_message(query.from_user.id, text, reply_markup=keyboard_markup)


@dp.callback_query_handler(text='/complaint_in_bot', state=TestStates.LOST_THING)
@dp.callback_query_handler(text='/complaint_other', state=TestStates.LOST_THING)
async def complaint(query: types.CallbackQuery):
    answer_data = query.data
    # always answer callback queries, even if you have nothing to say
    if answer_data == '/complaint_other':
        text = '''Контакты перевозчика:
    +7 (473) 259-75-92
    +7 (473) 232-02-65
    patp1vrn@yandex.ru'''
        await bot.send_message(query.from_user.id, text)
    if answer_data == '/complaint_in_bot':
        message_ = '''Оставьте обращение по следующему образцу (отправьте одним сообщением):
1⃣ Номер автобуса
2⃣ Госномер (если помните)
3⃣ В какой части автобуса
4⃣ Краткое описание вещи
5⃣ Ваш номер телефона или почта'''
        state = dp.current_state(user=query.from_user.id)
        await state.set_state(TestStates.all()[2])
        await bot.send_message(query.from_user.id, message_)


@dp.callback_query_handler(text='/complaint_in_bot', state=TestStates.MAIN_MENU)
@dp.callback_query_handler(text='/complaint_other', state=TestStates.MAIN_MENU)
async def complaint(query: types.CallbackQuery):
    answer_data = query.data
    # always answer callback queries, even if you have nothing to say
    if answer_data == '/complaint_other':
        text = '''Контакты перевозчика:
    +7 (473) 259-75-92
    +7 (473) 232-02-65
    patp1vrn@yandex.ru'''
        await bot.send_message(query.from_user.id, text)
    if answer_data == '/complaint_in_bot':
        state = dp.current_state(user=query.from_user.id)
        message_ = '''Оставьте обращение по следующему образцу (отправьте одним сообщением):
1⃣ Номер автобуса
2⃣ Госномер (если помните)
3⃣ Ваше сообщение
4⃣ Ваш номер телефона или почта
'''
        await state.set_state(TestStates.all()[1])
        await bot.send_message(query.from_user.id, message_)


@dp.message_handler(state=TestStates.COMPLAINT_IN_BOT)
async def complaint_text(message: types.Message):
    if message.text not in CHECK_LIST:
        msg['Subject'] = 'Жалоба или предложение [сообщение из telegram]'
        msg.attach(MIMEText(message.text, 'plain'))
        smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
        smtpObj.starttls()
        smtpObj.login('login', 'parol')
        smtpObj.sendmail(msg['From'], msg['To'], msg.as_string())
        await bot.send_message(message.from_user.id, 'Спасибо, Ваша жалоба будет передана службе поддержки')
        state = dp.current_state(user=message.from_user.id)
        await state.set_state(TestStates.all()[3])
    else:
        await bot.send_message(message.from_user.id, 'Чтобы выйти из "Жалобы и предложения" нажмите на любую кнопку')
        state = dp.current_state(user=message.from_user.id)
        await state.set_state(TestStates.all()[3])


@dp.message_handler(state=TestStates.LOST_THING)
async def complaint_text(message: types.Message):
    if message.text not in CHECK_LIST:
        msg['Subject'] = 'Забыли вещь [сообщение из telegram]'
        msg.attach(MIMEText(message.text, 'plain'))
        smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
        smtpObj.starttls()
        smtpObj.login('login', 'parol')
        smtpObj.sendmail(msg['From'], msg['To'], msg.as_string())
        await bot.send_message(message.from_user.id, 'Спасибо, скоро с Вами свяжутся наши сотрудники')
        state = dp.current_state(user=message.from_user.id)
        await state.set_state(TestStates.all()[3])
    else:
        await bot.send_message(message.from_user.id, 'Чтобы выйти из "Забыли вещь" нажмите на любую кнопку')
        state = dp.current_state(user=message.from_user.id)
        await state.set_state(TestStates.all()[3])


async def shutdown(dispatcher: Dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_shutdown=shutdown)
