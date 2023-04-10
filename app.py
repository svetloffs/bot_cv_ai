import telebot
from telebot import types
import os
import pathlib
from my_utils import config
from my_utils import mashrooms as mr
from my_utils.wiki import WikiArticle
from pprint import pprint

bot = telebot.TeleBot(config.APIKEY)

PHOTO_PATH = './photo_users'

os.makedirs(PHOTO_PATH, exist_ok=True)
mashrooms_dict = mr.mashrooms_dict
# mashrooms_dict[0]
item = mashrooms_dict[-1]['rus']
# item

def wiki_article_info(item, language='ru'):
    page = WikiArticle(item, language)
    # page = WikiArticle('World', 'ru')
    # page = WikiArticle('Волоконница звёздчатоспоровая', 'ru')
    article = page.get_article_wiki()
    img_links = page.get_images_links()
    print(img_links)
    print(article.categories)
    content = [i for i in article.content.split('\n') if i!='']
    sections_article = [i for i in article.content.split('\n') if i!='' and i.startswith("==")]

    if isinstance(img_links, list):
        [page.read_wiki_images(link, show_image=True) for link in img_links]
    else:
        page.read_wiki_images(img_links, show_image=True)
    return content

@bot.message_handler(commands=['edit'])
def edit(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("🇷🇺 Русский")
    btn2 = types.KeyboardButton('🇬🇧 English')
    markup.add(btn1, btn2)
    bot.send_message(
        message.from_user.id, 
        "🇷🇺 Выберите язык / 🇬🇧 Choose your language", reply_markup=markup)

#############################################################
#############################################################
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("👋 Поздороваться")
    markup.add(btn1)
    bot.send_message(
        message.from_user.id, 
        "👋 Привет! Я твой бот-помошник!", 
        reply_markup=markup)
#############################################################
#############################################################
@bot.message_handler(commands=['predict'])
def predict(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Run")
    markup.add(btn1)
    bot.send_message(
        message.from_user.id, 
        "Begin predict your image", 
        reply_markup=markup)
#############################################################
#############################################################
@bot.message_handler(content_types=['text'])
def get_text_messages(message):

    if message.text == '👋 Поздороваться':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True) #создание новых кнопок
        btn1 = types.KeyboardButton('Распознать❓')
        # btn2 = types.KeyboardButton('Правила сайта')
        # btn3 = types.KeyboardButton('Советы по оформлению публикации')
        # markup.add(btn1, btn2, btn3)
        markup.add(btn1)
        bot.send_message(
            message.from_user.id, 
            # '❓ Задайте интересующий вопрос', 
            'Отправляю...', 
            reply_markup=markup) #ответ бота
    # elif message.text == 'Правила сайта':
    #     bot.send_message(
    #         message.from_user.id, 
    #         'Прочитать правила сайта вы можете по ' + '[ссылке](https://habr.com/ru/docs/help/rules/)', 
    #         parse_mode='Markdown')

    # elif message.text == 'Советы по оформлению публикации':
    #     bot.send_message(
    #         message.from_user.id, 
    #         'Подробно про советы по оформлению публикаций прочитать по ' + '[ссылке](https://habr.com/ru/docs/companies/design/)', 
    #         parse_mode='Markdown')
#############################################################
#############################################################
@bot.message_handler(content_types=['photo', 'text'])
def photo(message):
    print(f"User ID: {message.from_user.id}\n"
          f"User UserNick: {message.from_user.username}\n"
          f"User FirstName: {message.from_user.first_name}\n"
          f"User LastName: {message.from_user.last_name}\n")

    print('message.caption =', message.caption)
    print('message.text =', message.text)
    print('message.photo =', message.photo)
    fileID = message.photo[-1].file_id
    print('fileID =', fileID)
    file_info = bot.get_file(fileID)
    print('file.file_path =', file_info.file_path)
    print('file.info =', file_info.file_unique_id)
    pprint('message.photo:\n', message.photo[-1])
    downloaded_file = bot.download_file(file_info.file_path)
    msg_cap = '' if message.caption is None else message.caption
    output_path = f"{PHOTO_PATH}/uid{str(message.from_user.id)}"
    os.makedirs(output_path, exist_ok=True)
    with open(f"{output_path}/{file_info.file_unique_id}_{msg_cap.replace(' ', '_')}.jpg", 'wb') as new_file:
        new_file.write(downloaded_file)
#############################################################
#############################################################
# photo = open('/tmp/photo.png', 'rb')
# bot.send_photo(chat_id, photo)
# bot.send_photo(chat_id, "FILEID")

if __name__ == "__main__":
    print("[INFO] Bot started..")
    bot.polling(none_stop=True, interval=0)