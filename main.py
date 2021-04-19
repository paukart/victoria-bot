#Библиотека для работы с VK_Api
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
#Генерация рандомных чисел типа int.
from random import randint
import time
# Библиотека для парсинг сайта с кроссвордами
from selenium import webdriver
from bs4 import BeautifulSoup
import settings

def main():

    vk_session = vk_api.VkApi(settings.login, settings.password, app_id=2685278)

    try:
        vk_session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return

    longpoll = VkLongPoll(vk_session)

    vk = vk_session.get_api()

    options = webdriver.ChromeOptions()
    options.add_argument('headless')  # для открытия headless-браузера
    browser = webdriver.Chrome(executable_path=settings.chromedriver, chrome_options=options)



    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            print('Новое сообщение:')
            if event.from_me:
                print('От меня для: ', end='')
            elif event.to_me:
                print('Для меня от: ', end='')
            if event.from_user:
                print(event.user_id)
            elif event.from_chat:
                print(event.user_id, 'в беседе', event.chat_id)
                print('Текст: ', event.text)
                if (event.user_id == -170763395):
                    stroka = event.text
                    stroka.lstrip()
                    if (stroka.find('букв') != -1 and stroka.find('Викторина запущена!') == -1):
                        desc_temp = ''
                        desc = ''
                        mask = stroka[stroka.find('•')-2]
                        mask_count = stroka.count('•')
                        print('Кол-во букв: ', mask, end='\n')
                        for i in range(0, len(stroka)):
                            if (stroka[i] == ' ' and stroka[i+1] == '('):
                                break
                            desc_temp += stroka[i]
                        desc = desc_temp.replace(' ', '%20')
                        desc = desc.replace('&quot;', '"')
                        print ('Вопрос: ', desc_temp, end='\n')
                        link = 'https://poncy.ru/crossword/?mask='+mask+'-'*mask_count+'&desc='+desc
                        browser.get(link)
                        requiredHtml = browser.page_source
                        soup = BeautifulSoup(requiredHtml, 'html.parser')
                        result = soup.find(id="helphref1")
                        if (result):
                            time.sleep(0.5)
                            vk.messages.send(peer_id = 2000000000 + event.chat_id, message =  result.text[0:mask_count+1].capitalize(), random_id = randint(0, 23000))
                        else:
                            print ('Не нашёл ответа :(')
            print()

if __name__ == '__main__':
    main() 