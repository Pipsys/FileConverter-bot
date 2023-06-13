import aiogram
import pytesseract
import cv2
import os
from aiogram import Bot, types, executor, Dispatcher
from pdf2image import convert_from_path
from pdf2docx import Converter
from PIL import Image
from config import API_TOKEN
from button import *
import pdf2docx

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
media = 0

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    mess_bot = f'Здравствуйте, <b>{message.from_user.first_name} {message.from_user.last_name}</b>, что хотите сделать?'
    await bot.send_photo(message.chat.id, types.InputFile('./ConvBaner.png'), caption= mess_bot, parse_mode = 'html',reply_markup = await mainKB())
@dp.callback_query_handler()
async def work(call : types.CallbackQuery):
    
    print(call.data)
    if '@work' in call.data:
        if 'фото' in call.data:
            await call.message.answer('Для того чтобы работать с фото выберите функционал', reply_markup = await photoKD())#show_alert=True
        elif 'видео' in call.data:
            await call.message.answer('Для того чтобы работать с видео выберите функционал',  reply_markup = await videoKB())
        elif 'документами' in call.data:
            await call.message.answer('Для того чтобы работать с документами выберите функционал',  reply_markup = await docKB())
    elif "@photo" in call.data:
        if 'Сканировать фото' in call.data:
            await call.message.answer(f'Пришлите мне фото')
            global media
            media = 1         
        if 'Конвертировать PNG в JPG' in call.data:
            await call.message.reply(f'Пришлите мне PNG фото и конвертирую его в JPG')
            media = 2
    elif '@doc' in call.data:
        if 'Сканировать PDF' in call.data:
            await call.message.answer(f'Пришлите мне PDF')
            media = 3
        if 'Конвертировать PDF в DOCX' in call.data:
            await call.message.answer(f'Пришлите мне PDF, который хотите конвертировать в DOCX')
            media = 4
    if '<back' in call.data:
        await call.answer('Вы вернулись в главное меню')
        await call.message.answer('Выберите функционал', reply_markup = await mainKB()) 

@dp.message_handler(content_types=types.ContentType.ANY)
async def load(message: types.Message):
    if message.content_type == 'photo':
        if media == 1:
            path = str(f'./Photo_Container\photo_{message.chat.id}.png')
            await message.photo[-1].download(destination_file=path)
            print('Фото сохранено в ' + path)   
            img = cv2.imread(path)
            string = pytesseract.image_to_string(img, lang='rus+eng')
            await message.reply(string) 
            os.remove(path)
            print('Фото удалено из ' + path)    
            await message.answer('Сканирование успешно завершено', reply_markup = await backmenuKB())
        elif media == 2:
            mess_id = message.chat.id
            path = './Photo_Container\png_in_jpg\png_'+str(mess_id)+'.png'
            print('Путь к фалу получен')
            await message.photo[-1].download(destination_file=path)
            print('Файл PNG скачен')
            print(message.chat.id)
            im1 = Image.open(path)
            im1.save(path + '.jpg')  
            await bot.send_photo(mess_id, photo=im1)    
    elif message.content_type == 'document':
        if media == 3:
            doc = message.document.file_id
            print('файл получен')
            path = path = f'D:\Python\DevConverterBot\PDF_Container\PDF_{doc}.pdf' 
            await message.document.download(destination_file=path)
            print('Файл сохранен в ' + path)
            images = convert_from_path(path, 500, poppler_path=r'C:\Program Files\poppler-0.68.0\bin')
            for i, image in enumerate(images):
                fname = f'D:\Python\DevConverterBot\PDF_Container\PDF_in_PNG\image{str(i)}.png'
                image.save(fname, "PNG")
                print('Фото файла pdf сохранено в ' + fname)
            img = cv2.imread(fname)
            string = pytesseract.image_to_string(img, lang='rus+eng')
            await message.reply(string)
            os.remove(path)
            os.remove(fname)
            print(f'Фото и фалы удалены из {path} и {fname}')
            await message.answer('Сканирование успешно завершено', reply_markup = await backmenuKB())
        elif media == 4:        
            pdf_file = 'D:\Python\DevConverterBot\_test.pdf'
            docx_file = 'D:\Python\DevConverterBot\_sample.docx'
            print('файлы получены')

            cv = Converter(pdf_file)
            cv.convert(docx_file)      
            cv.close()
            print('Файлы  успешно конвертировались!')
            await message.reply_document(open('D:\Python\DevConverterBot\_sample.docx', 'rb'))

if __name__ == '__main__':  
    executor.start_polling(dp)