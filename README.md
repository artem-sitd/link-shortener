# Содержание

1. [Краткое описание проекта](#summary)
2. [Установка](#install)
    3. [Локальная установка](#local_install)
    4. [Видеодемонстрация локальной установки](#video_local)
    5. [Установка на ваш сервер](#install_vps)
    6. [Видеодемонстрация установки на вашем сервере](#video_vps)

3. [Детальное описание проекта](#detail_summary)

4. [Идеи для улучшения](#idea)

5. [Общие Полезные команды](#commands)

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
   <li> Получите api-key у бота <code>@BotFather</code>.</li>
   <li>Клонируйте репозиторий <code>git clone https://github.com/artem-sitd/link-shortener.git</code></li>
   <li>Переименуйте файл <code>env.local.template</code> в <code>.env.local</code>., вставьте ваш api-key напротив переменной 
<code>telegram_api_key</code> после знака <code>=</code>.
   Должно получиться что-то вроде <code>telegram_api_key=7711111VjMsdf5801:A74hGffoOomZMsPJTdoH_jbLIR6A4q8_bM3jM</code></li>
   <li>В модуле <code>settings.py</code> в функции <b>get_env_file</b> необходимо присвоить переменной <b>local</b>
 значение <b>True</b>, для использования правильного 
 файла для переменных окружения. Должно получиться: <code>def get_env_file(local: bool = True) -> Path:</code></li>
<li>В связи с тем, что телеграмм может отправлять вебхуки только на публичный <code>https</code> домен, 
для локального тестирования воспользуемся <code>localtunnel</code>. Для установки <code>localtunnel</code>: 
вставьте в терминал <code>npm install -g localtunnel</code>. 
<p><b>Если у вас нет пакетного менеджера npm, установите его командой: <code>sudo apt install npm </code></b>.</p> 
После установки <code>localtunnel</code> получим временный публичный <u>https url</u>, командой: 
<code>lt --port 8082</code> <i>(указал не стадратный порт на случай, если ваш 8080 уже чем-то занят, и дабы не заниматься поисками
- сразу зададим свободный порт)</i>, который будет проксировать входящие запросы к нам на локальный сервер.</li>
Полученный url необходимо вставить в файл <code>.env.local</code> в переменную <code>WEBHOOK_HOST</code>.
Должно получиться примерно: <code>WEBHOOK_HOST=https://strong-chairs-drive.loca.lt</code>
   <li>Убедитесь, что в файле <code>docker-compose.yml</code> для сервиса <b>bot</b> указаны порты: <code>8082:8080</code></li>
   <li>Локальная установка завершена и можно запускать контейнеры. Перейдите в директорию с проектом и вводите команду 
<code>docker-compose up --build</code>. Для тестирования функционала обратитесь к боту, вводя валидные url адреса</li>
</ol>

<h3 id="video_local">Видеодемонстрация локальной установки</h3>
> будет позже

<h3 id="install_vps">Установка на ваш сервер</h3>
Прежде чем начать - вам необходим ваш VPS/VDS, домен с https (получение TLS / SSL есть исчерпывающие инструкции в интернете).
Установка предполагается на чистую систему.
<ol>
<li>Касательно настроек хостового Nginx: Во-первых указываете путь к SSL сертификатам, далее необходимо вставить проксирование 
запросов на наши ручки контейнерного веб приложения. Учитывайте момент, что если у вас работает несколько контейнеров - 
указывайте разные порты, но я предполагаю, что расписывать как это работает - будет неуместно в описании данного проекта. Во-вторых, предлагается указать следующую маршрутизацию:
</li>
<li> Получите api-key у бота <code>@BotFather</code>.</li>
<li>Клонируйте репозиторий <code>git clone https://github.com/artem-sitd/link-shortener.git</code></li>
<li>Переименуйте файл <code>env.template</code> в <code>.env</code>., вставьте ваш api-key напротив переменной 
<code>telegram_api_key</code> после знака <code>=</code>.
   Должно получиться что-то вроде <code>telegram_api_key=7711111VjMsdf5801:A74hGffoOomZMsPJTdoH_jbLIR6A4q8_bM3jM</code></li>
<li></li>
<li></li>
</ol>


<h3 id="video_vps">Видеодемонстрация установки на вашем сервере</h3>
> будет позже

<h2 id="detail_summary">Детальное описание проекта</h2>
Маршрут запросов выглядит следующим образом: указывая телеграму адрес вебхуков, сообщения приходят на хостовой nginx,
который проксирует запрос на указанный порт и адрес (в нашем случае http:localhost:8080), ничего страшного в том, что
запросы между контейнерами внутри сервера идут по http, т.к. в монго сохраняется отдельно протокол, отдельно хэш.
В случае редиректа - мы собираем ссылку из: протокола, нашего домена и хэша.
Переходя по короткой ссылке поиск осуществляется по хэшу (после /s/)

<h2 id="idea">Идеи для улучшения</h2>
<ul>
<li>Настройка логирования в файл / терминал</li>
<li>Подключение grafana , prometheus</li>
<li>Настройка корректных перезапусков контейнеров</li>
<li>Добавить поле с указанием id пользователя</li>
<li>Добавить функционал с кнопкой в телеграмме о количестве сохраненных ссылок, датах у пользователя</li>

</ul>


<h2 id="commands">Общие Полезные команды</h2>

В случае выявление не точностей в этом файле или в целом в проекте tg: `@art_kak_dela`


<ul> 
<li>Установка вебхуков <code>npm install -g localtunnel</code></li>
<li>Получение локальных вебхуков: <code>lt --port 8080</code></li>
<li> <code></code></li>
<li> <code></code></li>
<li> <code></code></li>

</ul>

1. настройка хостового Nginx
2. Вебхуки отправляются только на https
3. Создание сети докера в ручную, для проксирования nxinx-ом сразу в контейнер по имени container_name,
   указанным в докер компос
4. в докер компос указать название сети для каждого контейнера + глобально + external
