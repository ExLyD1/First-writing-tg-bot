from env import *

from telethon import TelegramClient, events
from telethon.tl.types import (
    PeerUser, 
    ReplyKeyboardMarkup, 
    ReplyInlineMarkup, 
    KeyboardButtonRow, 
    KeyboardButton,
    KeyboardButtonUrl,
    KeyboardButtonCallback
)

from my_captcha import Captcha
from datetime import timedelta


bot = TelegramClient('bot', API_ID, API_HASH).start(bot_token=API_TOKEN)


wait_captcha = {}
isVerify = False

bad_words = [
    'чурка',
    'z',
    'v',
    'з'
]

bad_guys = {}



@bot.on(events.NewMessage(pattern='/start'))
async def start(event):

    keyboard_buttons = ReplyKeyboardMarkup(
        [
            KeyboardButtonRow( 
                [
                    KeyboardButton(text="Меню"),
                    KeyboardButton(text="Butt"),
                ]
            ),
        ]
    )

    await bot.send_message(
        entity=event.sender_id,
        message="Тыкни кнопку меню",
        buttons=keyboard_buttons,
    )


    user_entity = await event.get_sender()  

    if user_entity.username is not None:
        greetings = '@' + user_entity.username
    else:
        greetings = user_entity.first_name

    captcha = Captcha()

    await bot.send_message(
        entity=event.sender_id,  
        message=f'Привет, {greetings}, введи капчу',
        file = captcha.captcha_image
    )
    
    wait_captcha[user_entity.id] = captcha.captcha_text


@bot.on(events.NewMessage(pattern="Меню"))
async def menu(event):
    inline_buttons = ReplyInlineMarkup(
        [
            KeyboardButtonRow(
                [
                    KeyboardButtonUrl(
                        text="check the code github",
                        url="https://github.com/ExLyD1"
                    ),
                    KeyboardButtonCallback(
                        text='Say THX',
                        data=b'thanks'
                    )
                ]
            )
        ]
    ) zxc

    await bot.send_message(
        entity=event.sender_id,
        message="Тыкни кнопку меню",
        buttons=inline_buttons,
    )



@bot.on(events.CallbackQuery(data=b'thanks'))
async def thanks(event):
    await event.respond('siski popa <3')


@bot.on(events.NewMessage())
async def new_message(event):


    if event.text == '/start':
        return
        
    user_id = event.sender_id 

    user_entity = await event.get_sender()

    captcha = wait_captcha.get(user_id)


    if captcha is not None:
        if event.text != captcha:  
            await event.respond('Введено неверно, по новой:')  
        else:
            await event.respond(f'Добро пожаловать, {user_entity.first_name}!') 
            del wait_captcha[user_id]  

    if any(bad_word in event.text.lower() for bad_word in bad_words):

        if not bad_guys.get((user_entity.id, event.chat_id)):
            bad_guys[(user_entity.id, event.chat_id)] = 1
        else:
            bad_guys[(user_entity.id, event.chat_id)] += 1

        await bot.delete_messages(
            entity=event.chat_id,
            message_ids=[event.message]
        )

        match bad_guys[(user_entity.id, event.chat_id)]:
            case 1:
                await bot.send_message(
                    entity=event.chat_id,
                    message=f'@{user_entity.username} не пиши хуйні, некст раз мут'
                )
            case 2: 
                await bot.edit_permissions(
                    entity=event.chat_id,
                    user=user_id,
                    send_messages=False,
                    until_date=timedelta(seconds=10)
                )
                await bot.send_message(
                    entity=event.chat_id,
                    message=f'@{user_entity.username} лови мут на 10 секунд, некст раз кік'
                )
            case 3:
                await bot.kick_participant(
                    entity=event.chat_id,
                    user=user_id,
                    message=f'@{user_entity.username}был кикнут'
                )
        if bad_guys[(user_entity.id, event.chat_id)] > 3:
            await bot.send_message(
                entity=event.chat_id,
                message=f'@{user_entity.username}, не пиши хуйні.'
            )


# @bot.on(events.NewMessage)
# async def handler(event):
#     # Проверяем, переслано ли сообщение
#     if event.message.forward:
#         # Получаем информацию о пересланном сообщении
#         forward_sender_id = event.message.forward.sender_id  # ID отправителя пересланного сообщения
        
#         if forward_sender_id:
#             forward_sender = await bot.get_entity(forward_sender_id)  # Получаем объект отправителя
            
#             if forward_sender.username:
#                 await event.respond(f"Username пересланного сообщения: @{forward_sender.username}")
#             else:
#                 await event.respond("У этого пользователя нет username.")
#         else:
#             await event.respond("Не удалось получить ID пересланного сообщения.")
#     else:
#         # Если сообщение не переслано, получаем отправителя обычного сообщения
#         sender = await event.get_sender()
        
#         if sender.username:
#             await event.respond(f"Username отправителя: @{sender.username}")
#         else:
#             await event.respond("У этого пользователя нет username.")



# @bot.on(events.NewMessage())
# async def test(event):
#     await event.respond(event.message.text) #текст сообщения

#     await event.reply('reply') # отвечает мне на сообщение

#     await event.respond(str(event.sender_id)) # берет айди отправителя

#     await event.respond(str(event.chat_id)) # берет айди чата

#     sender = await event.get_sender() # берет инфу об отправителе
#     await event.respond(f"Sender: {sender.username}") 

#     await event.respond(str(event.is_private)) # приватный/нет
#     await event.respond(str(event.is_group)) # група/нет

#     # await event.delete()
#     await event.forward_to(event.chat_id) # пересылает сообщение


#     sender_id = event.from_id # берет айди отправтиля
#     sender = await event.client.get_entity(sender_id) # так же инфа о отправителе
#     print(f"Отправитель: {sender.username}")


def main():
    bot.run_until_disconnected()

if __name__ == '__main__':
    main()
