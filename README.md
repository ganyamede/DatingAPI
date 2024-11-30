![telegram-cloud-photo-size-2-5357177841936100860-y](https://github.com/user-attachments/assets/b211bacc-f94f-4ce0-aa87-98b9aa52d632)# DatingAPI

Проект **Dating API** представляет собой backend для платформы знакомств, построенный с использованием **Flask**, **SQLAlchemy**, **JWT** и **Redis**. Этот проект включает в себя RESTful API для аутентификации пользователей, управления профилями, сообщениями и лайками, а также интеграцию с **Swagger UI** для удобного тестирования и документации.

## Особенности

- **JWT** для безопасной аутентификации и управления сессиями.
- **SQLAlchemy** для работы с базой данных, хранящей информацию о пользователях, сообщениях и лайках.
- **Redis** для кеширования и улучшения производительности.
- **Flask** — легковесный фреймворк для разработки REST API.
- **Swagger UI** для интерактивной документации и тестирования API.

## Установка

1. Клонируйте репозиторий:

   ```bash
   git clone https://github.com/ganyamede/DatingAPI.git
   cd DatingAPI
   ```

2. Создайте и активируйте виртуальное окружение:

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Для macOS/Linux
   venv\Scriptsctivate  # Для Windows
   ```

3. Установите зависимости:

   ```bash
   pip install -r requirements.txt
   ```

4. Запустите приложение:

   ```bash
   python3 main.py
   ```

5. Откройте [Swagger UI](http://localhost/apidocs) для тестирования API.


6. Детальное описание проекта, документация

   ### Везде необходимо использовать JWT ACCESS TOKEN
   ### Kроме блока Authentication и Utility в документации на фото ниже

   # Utility
   ![telegram-cloud-photo-size-2-5357177841936100849-y](https://github.com/user-attachments/assets/8fa4ae21-516b-4898-82d5-97c9978d3576)

   - Получение всех городов страны
   - Работает с одной страной, возможно расширение

   # Authentication
     ## Register
     ![telegram-cloud-photo-size-2-5357177841936100856-y](https://github.com/user-attachments/assets/cf716d3c-c07a-4635-bbd3-f8101769a347)

     - Регистрация профиля
     - Мы не возвращаем JWT токен тут, мы заносим данные в бд и после ожидам уже вход в localhost/api/sign
     - Одностороннее шифрование пароля, после сверяем
  
     ## Sign
     ![telegram-cloud-photo-size-2-5357177841936100859-y](https://github.com/user-attachments/assets/2772f20e-7858-4c85-84d7-65e3ea4c64f8)

     - После входа вы возвращаем access/refresh token который желательно сразу записать в httpOnly

     ## Refresh to access
     ![telegram-cloud-photo-size-2-5357177841936100854-y](https://github.com/user-attachments/assets/f87bc240-e602-4940-a3c9-69adad4bcb42)

     - Получаем информацию что записано в Refresh и записываем в access
     - Подходит если срок службы access завершился
  
  # Match
   ## MatchAll
   ![telegram-cloud-photo-size-2-5357552337314507948-y](https://github.com/user-attachments/assets/9c5f905c-4811-49b9-9b5f-64e79dc49be3)

   - Список всех взаимных симпатий

   ## Search
   ![telegram-cloud-photo-size-2-5357177841936100851-y](https://github.com/user-attachments/assets/ed6ffe8c-2af2-446f-8a84-82b61e532927)

   - Ищем вам партнера по критериям
   - Получаем вашу информацию и ищем вам пару по ней, если она была найдена получаем ваши города, переобразовываем в lat/long и считаем в км, если дистанция менее 30 км тогда возвращаем

   ## Get like
   ![telegram-cloud-photo-size-2-5357177841936100850-y](https://github.com/user-attachments/assets/95e88648-9f97-4224-9e94-1ff9edca4511)

   - Список всех кто вас лайкнул

  # Likes
   ## Like
   ![telegram-cloud-photo-size-2-5357177841936100852-y](https://github.com/user-attachments/assets/bdf59b71-7b10-4fcd-b4ea-0242d130cfb2)
   
   - Записываем лайк в базу данных, после отображаем в списке лайкнувших для принятие решения
   - Так же лайк записываем в Redis, что бы больше не попадался в течении 24ч

   ## Dislike
   ![telegram-cloud-photo-size-2-5357177841936100853-y](https://github.com/user-attachments/assets/c6bb8088-20f9-4f4f-8e86-917993076f87)

   - Пропускаем анкету, так же как и с лайком записываем в Redis что бы не повторялись
   - В случае если это тебя лайкнули, тогда мы еще удаляем запись из БД

  # Client
   ## Select
   ![telegram-cloud-photo-size-2-5357177841936100860-y](https://github.com/user-attachments/assets/b3f83deb-3f48-42c3-ac07-dd22555251f7)

   - Получаем полную информацию о вашей анкете, для вывода в профиль
   - Исключительно об анкете, не почта и не пароли.
   - id/age/name/city/description/sex/search_sex/user_id (id аккаунта, где почта)

   ## Update
   ![telegram-cloud-photo-size-2-5357177841936100861-y](https://github.com/user-attachments/assets/8295c412-3f52-4861-8efc-30ecaf3620fc)

   - Создание анкеты или обновление информации, данные передают одинаково, проверка на то имеется ли аккаунт происходит внутри
   - До 6 фоток, обязательно передавать age/name/city/description/sex/search_sex

  



  

  


     
      

     
   

## Лицензия

Этот проект лицензирован под MIT License — см. [LICENSE](LICENSE) для подробностей.

