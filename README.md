# Содержание
1. [Краткое описание проекта](#summary)
2. [Установка](#install)
   3. [Локальная установка](#local_install)
   4. [Видеодемонстрация локальной установки](#video_local)
   5. [Установка на ваш сервер](#install_vps)
   6. [Видеодемонстрация установки на вашем сервере](#video_vps)

3. [Детальное описание проекта](#detail_summary)

4. [Идеи для улучшения](#idea)

5.  [Общие Полезные команды](#commands)
------------------

<h2 id="summary">Краткое описание проекта</h2>
Проект призван отдавать пользователю (через бота телеграм) сокращенный вариант длинной ссылки. 
Аналогичный функционал реализован на проектах: Vk.com/cc, Lnnkin, U.to, Bit.do, Bitly.com, Ow.ly и прочие.
Пользователь пишет боту длинный URL, в ответ бот присылает сокращенную ссылку, при переходе по ней - 
происходит редирект по адресу оригинальной ссылки.

Используемые технологии: Python3.9+, aiogram3.17, Mongodb, aiohttp, docker. Весь список в requirements.txt
<h2 id="install">Установка</h2>

<h3 id="local_install">Локальная установка</h3>
<ol> 
   <li> Получите api-key у бота <code>@BotFather</code>. </li>
   <li>Клонируйте репозиторий <code>git clone</code></li>
   <li>Переименуйте файл <code>env.local.template</code> в <code>.env.local</code>., вставьте ваш api-key напротив переменной 
<code>telegram_api_key</code> после знака <code>=</code>.
   Должно получиться что-то вроде <code>telegram_api_key=7711111VjMsdf5801:A74hGffoOomZMsPJTdoH_jbLIR6A4q8_bM3jM</code></li>
   <li>В связи с тем, что телеграмм может отправлять вебхуки только на публичный <code>https</code> сервер, 
для локального тестирования воспользуемся <code>localtunnel</code>. Для установки <code>localtunnel</code>: 
вставьте в терминал <code>npm install -g localtunnel</code>. 
<p><b>Если у вас нет пакетного менеджера npm, установите его командой: <code>sudo apt install npm </code></b>.</p> 
После установки <code>localtunnel</code> получим временный публичный <u>https url</u>, командой: 
<code>lt --port 8080</code>который будет проксировать входящие запросы к нам на локальный сервер на порт 8080.</li>
Полученный url необходимо вставить в файл <code>.env.local</code> в переменную <code>WEBHOOK_HOST</code>.
Должно получиться примерно: <code>WEBHOOK_HOST=https://strong-chairs-drive.loca.lt</code>

   <li></li>
   <li></li>

</ol>



<h3 id="video_local">Видеодемонстрация локальной установки</h3>
`будет позже`

<h3 id="install_vps">Установка на ваш сервер</h3>

<h3 id="video_vps">Видеодемонстрация установки на вашем сервере</h3>
`будет позже`

<h2 id="detail_summary">Детальное описание проекта</h2>

<h2 id="idea">Идеи для улучшения</h2>

<h2 id="commands">Общие Полезные команды</h2>




Установка вебхуков
`npm install -g localtunnel`

Получение локальных вебхуков:
`lt --port 8080`

