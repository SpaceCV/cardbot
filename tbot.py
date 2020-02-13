from config import TELEGRAM_TOKEN, ALL_CARDS
from telebot import types
import telebot
import random
from PIL import Image
from io import BytesIO
from math import ceil

class Tbot():
    def send(self, id, text, r):
        try:
            if r == 0 or r == False:
                self.bot.send_message(id, text)
            else:
                self.bot.send_message(id, text, reply_markup=r)
        except telebot.apihelper.ApiException:
            return False

    def __init__(self):

        self.bot = telebot.TeleBot(TELEGRAM_TOKEN)
        self.default_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        self.default_keyboard.add("Задать вопрос БОТу Тарологу")


        @self.bot.message_handler(commands=["start"])
        def t_start(m):
            print(m)
            #keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            #keyboard.add("Задать вопрос БОТу Тарологу")
            #keyboard.add("Ydfngldfjg")
            self.bot.send_message(chat_id=m.chat.id, text="Привет, " + m.chat.first_name, reply_markup=self.default_keyboard)
            # в какой диалог отправить, что отправить, клавиатура
            return True

        @self.bot.message_handler(func=lambda message: True)
        def t_all(m):
            if m.text == "Задать вопрос БОТу Тарологу":
                keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                keyboard.add("Отношения с ...")
                keyboard.add("Анализ да/нет")
                self.send(m.chat.id, "Выберите тему вопроса", keyboard)
            elif m.text == "Отношения с ...":
                keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                keyboard.add("Сделать расклад")
                keyboard.add("Назад")
                self.send(m.chat.id,"Загадайте человека. Раскад покажет, какое влияние эти отношения оказывают на вас",keyboard)
            elif m.text == "Назад":
                self.send(m.chat.id,"ghj",self.default_keyboard)
            elif m.text == "Сделать расклад":

                texts = [
                    '??? Как вы проявляетесь во взаимоотношениях с этим человеком?',
                    '??? Какие ваши качества активизируют эти взаимоотношения?',
                    '??? Какие ваши качества подавляют эти взаимоотношения?',
                    '??? Какова роль вашего партнера?',
                    '??? Чему учат эти взаимоотношения?',
                    '??? В каком направлении развиваются эти отношения?',
                ]

                cards_amount = len(texts)

                local_cards = set()

                image_in_row = 3
                image_dir = 'images/'

                while len(local_cards) < cards_amount:
                    r = random.randint(0, len(ALL_CARDS) - 1)
                    local_cards.add(r)

                local_cards = list(local_cards)
                random.shuffle(local_cards)

                image_paths = [image_dir + ALL_CARDS[i]['image'] for i in local_cards]

                images = list(map(Image.open, image_paths))

                rows = ceil(len(images) / image_in_row)

                image_h = images[0].size[1]
                image_w = images[0].size[0]

                h = image_h * rows
                w = image_w * image_in_row

                result = Image.new("RGB", (w, h), color='white')

                desc = []

                for i in range(rows):
                    for j in range(image_in_row):
                        result.paste(images[i * image_in_row + j], (j * image_w, i * image_h))
                        card = ALL_CARDS[local_cards[i * image_in_row + j]]
                        desc.append(texts[i * image_in_row + j])
                        desc.append(card['value'][random.randint(0, len(card["value"]) - 1)])

                img = BytesIO()
                result.save(img, 'PNG')
                self.bot.send_photo(m.chat.id, img.getvalue())
                self.send(m.chat.id,'\n\n'.join(desc),0)

            elif m.text == "Анализ да/нет":
                keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                keyboard.add("Сделать расклад Анализ")
                keyboard.add("Назад")
                self.send(m.chat.id,"Раскалад для вопросов в формате делать/не делать. Он покажет, как будут развиваться события, если вы примите решение делать, и как сложиться, если решите не делать. Даст рекомендацию для наилушего исхода события в одном м другом случае.", keyboard)
            elif m.text == "Назад":
                self.send(m.chat.id,"ghj",self.default_keyboard)
            else:
                t_start(m)
            return True

    def poll(self):
        self.bot.remove_webhook()
        self.bot.infinity_polling()
