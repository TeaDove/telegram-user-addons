# telegram-user-addons
Небольшой аддон для телеграмма, добавляющий несколько классных фичей

## !ping_all
При прописавыние данной комманды пингует всех пользователей в группе.

## Youtube to video 
При отсылке сообщения с ссылкой на ютуб видео конвертирует его 
в нативное телеграм видео, очень удобно

## Инструкция
1. Установите пакеты для питона ``pip3 install -r requirements.txt``
2. Создайте config.ini в папке secret_data по шаблону:<br>
<code>
[credentials]
pyrogram_api_id = *****
pyrogram_api_hash = *****</code><br>
3. Для запуска, пропишите из папки telegram-user-addons
`python3 start.py` 