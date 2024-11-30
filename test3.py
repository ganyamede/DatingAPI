import requests
import json
import random
from server.app import get_all_city
from faker import Faker

fake = Faker()


# Список имен для мужчин и женщин
male_names = ['Вадим', 'Максим', 'Александр', 'Иван', 'Олександр', 'Артем', 'Михайло', 'Дмитро', 'Петро', 'Сергій']
female_names = ['Олена', 'Марія', 'Ірина', 'Тетяна', 'Наталія', 'Катерина', 'Анна', 'Вікторія', 'Юлія', 'Оксана']

for _ in range(100):
    sex = random.choice([1, 2, 3])  # 1 - men, 2 - women, 3 - men and women
    search_sex = random.choice([1, 2])  # Пол поиска (1 - men, 2 - women)

    if sex == 1:  # Мужчина
        name = random.choice(male_names)
    elif sex == 2:  # Женщина
        name = random.choice(female_names)
    else:  # Пол смешанный
        name = random.choice(male_names + female_names)

    # Случайный возраст от 15 до 40
    age = random.randint(15, 40)

    # Случайный город из Украины
    city = random.choice(get_all_city('UA'))

    # Данные для отправки
    data = {
        "name": name,
        'age': age,
        'city': city,
        'description': fake.sentence(nb_words=6),  # Сгенерированное описание
        'sex': sex,
        'search_sex': search_sex
    }

    # Фотографии
    img_list = ['app/storage/img/photo1.jpg', 'app/storage/img/photo2.jpg']
    files = [('files', open(photo, 'rb')) for photo in img_list]

    gmail = f"{name.lower()}{random.randint(1000, 9999)}@gmail.com"

    register_response = requests.post(
        url='http://127.0.0.1/api/register',
        headers={"Content-Type": "application/json"},
        data=json.dumps({'gmail': gmail, 'password': '12345678'})
    )

    sign_response = requests.post(
        url='http://127.0.0.1/api/sign',
        headers={"Content-Type": "application/json"},
        data=json.dumps({'gmail': gmail, 'password': '12345678'})
    )

    access_token = sign_response.json()['key']['access_token']
    url = "http://127.0.0.1/api/update"
    headers = {"Authorization": f"Bearer {access_token}"}

    # Отправка запроса
    response = requests.post(url, headers=headers, data=data, files=files)

    # Печать ответа
    print(response.json())
