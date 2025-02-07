## 1. Описание проекта

Проект Blogicum - социальная сеть для публикации личных дневников.

Это сайт, на котором пользователь может создать свою страницу и публиковать на ней сообщения («посты»).

Для каждого поста нужно указать категорию, а также опционально локацию, с которой связан пост. 

Пользователь может перейти на страницу любой категории и увидеть все посты, которые к ней относятся.

Пользователи смогут заходить на чужие страницы, читать и комментировать чужие посты.

## 2. Стек проекта (список технологий):

Язык программирования: *Python*

Фреймворк: *Django*

База данных: *SQLite*

Системы контроля версий: *Git*

Инструменты разработки: *VSCode*

Управление зависимостями: *pip, requirements.txt*

## 3. Как запустить проект: 

Клонировать репозиторий и перейти в него в командной строке 
 
### Cоздать и активировать виртуальное окружение: 

Windows 

``` python -m venv venv ``` 
``` source venv/Scripts/activate ``` 

Linux/macOS

``` python3 -m venv venv ``` 
``` source venv/bin/activate ``` 

### Обновить PIP 
 
Windows 

``` python -m pip install --upgrade pip ``` 

Linux/macOS 

``` python3 -m pip install --upgrade pip ``` 
 
### Установить зависимости из файла requirements.txt: 
 
``` pip install -r requirements.txt ``` 
 
### Выполнить миграции: 
 
Windows 

``` python manage.py makemigrations ``` 
``` python manage.py migrate ``` 

Linux/macOS 

``` python3 manage.py makemigrations ``` 
``` python3 manage.py migrate ``` 

### Запустить проект: 

Windows 

``` python manage.py runserver ``` 

Linux/macOS 

``` python3 manage.py runserver ``` 


## 4. Автор проекта:

Плахотная Елена 

