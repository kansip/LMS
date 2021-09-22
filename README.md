## Описание проекта
Проект LMS (Learning Managment System) - то хранилище учебных материалов — видеоуроков, лекций, презентаций, книг и курсов, доступ к которым можно получить с любого устройства в любой точке мира.
## Запуск проекта
1) Создать папку с проектом
2) Открыть в BASH эту папку
3) Сделать команду `git clone https://github.com/kansip/ManageStudents ./`
4) В CMD создаем виртуальное окружение в рабочей директории для работы с Python `python -m venv venv`
5) В CMD запускаем консоль виртуального окружения `venv\Scripts\activate`
6) В CMD(venv) обновляем `pip install --upgrade pip`
7) Установить нужные версии пакетов командой `pip install -r requirements.txt`
8) Создаем миграцию базы данных `python manage.py migrate`
9) В CMD(venv) поднимаем сервер командой  `python manage.py runserver` теперь сайт висит на `localhost` c адресом `http://127.0.0.1:8000`