# Запуск проекта

## 1. Установите Git

Git необходим для клонирования репозитория проекта. Если у вас еще не установлен Git, скачайте и установите его с [официального сайта](https://git-scm.com/).

## 2. Клонируйте проект

Перейдите по следующему URL: [https://gitflic.ru/project/zov/product](https://gitflic.ru/project/zov/product). Вы можете либо скачать проект как архив, либо клонировать его с помощью команды:

```bash
git clone https://gitflic.ru/project/zov/product.git
  ```

## 3. Скачайте и установите Python 3.1
 Перейдите на официальный сайт Python и скачайте версию 3.10 : https://www.python.org/downloads/release/python-3100/. Установите Python, следуя инструкциям на экране.

 ## 4. Создайте виртуальное окружение

 После установки Python создайте виртуальное окружение. В командной строке выполните:

```bash
python -m venv venv
 ```
Активируйте виртуальное окружение:


```bash
venv\Scripts\activate
```

## 5. Перейдите в директорию проекта

## 6. Установите зависимости
Установите необходимые зависимости из файла requirements.txt с помощью команды:

```bash 
pip install -r requirements.txt 
```

## 7. Запустите сервер
Выполните команду для запуска сервера :
```bash 
python manage.py runserver
```
## 8. Готово!
Теперь вы можете открыть браузер и перейти по адресу http://127.0.0.1:8000/, чтобы увидеть ваш проект.