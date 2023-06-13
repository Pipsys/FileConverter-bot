from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# all_button=['Назад','Работа c фото', 'Работа c документами', 
#             'Работа c видео', 'Сканировать фото','Конвертировать PNG в JPG', 
#             'Сканировать PDF', 'Конвертировать MP4 в GIF']

async def mainKB():
    buttons = ['Работа c фото','Работа c видео',
                'Работа c документами']
#     btn = [InlineKeyboardButton(button, callback_data=f'@work_{button.split(" ")[2]}')
    btn = [InlineKeyboardButton(button, callback_data=f'@work_{button}')
            for button in buttons]
    cancel = InlineKeyboardButton('Back', callback_data='<back')
    inl_menu = InlineKeyboardMarkup(row_width=2).add(*btn)
    return inl_menu

async def photoKD():
        buttons = ['Сканировать фото', 
                        'Конвертировать PNG в JPG']
        btn = [InlineKeyboardButton(button, callback_data=f'@photo_{button}')
                for button in buttons]
        cancel = InlineKeyboardButton('Назад', callback_data='<back')
        inl_menu = InlineKeyboardMarkup(row_width=1).add(*btn).add(cancel)
        return inl_menu

async def videoKB():
        buttons = ['Конвертировать MP4 в GIF']
        btn = [InlineKeyboardButton(button, callback_data=f'@video_{button}')
                for button in buttons]
        cancel = InlineKeyboardButton('Назад', callback_data='<back')
        inl_menu = InlineKeyboardMarkup(row_width=1).add(*btn).add(cancel)
        return inl_menu

async def docKB():
        buttons = ['Сканировать PDF', 'Конвертировать PDF в DOCX']
        btn = [InlineKeyboardButton(button, callback_data=f'@doc_{button}')
                for button in buttons]
        cancel = InlineKeyboardButton('Назад', callback_data='<back')
        inl_menu = InlineKeyboardMarkup(row_width=1).add(*btn).add(cancel)
        return inl_menu

async def backmenuKB():
        buttons = ['Вернуться в главное меню']
        btn = [InlineKeyboardButton(button, callback_data=f'<back_{button}')
                for button in buttons]
        inl_menu = InlineKeyboardMarkup(row_width=1).add(*btn)
        return inl_menu