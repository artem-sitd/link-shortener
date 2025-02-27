# _27.02.2025 Данное руководство еще не завершено_

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
   <li>Переименуйте файл <code>env.local.template</code> в <code>.env.local</code>., вставьте ваш api-key напротив 
переменной 
<code>telegram_api_key</code> после знака <code>=</code>.
   Должно получиться что-то вроде <code>telegram_api_key=7711801:A74hGffoOomZMsPJTdoH_jbLIR6A4q8_bM3jM</code></li>
   <li>В модуле <code>settings.py</code> в функции <b>get_env_file</b> необходимо присвоить переменной <b>local</b>
 значение <b>True</b>, для использования правильного 
 файла для переменных окружения. Должно получиться: <code>def get_env_file(local: bool = True) -> Path:</code></li>
<li>В связи с тем, что телеграмм может отправлять вебхуки только на публичный <code>https</code> домен, 
для локального тестирования воспользуемся <code>localtunnel</code>. Для установки <code>localtunnel</code>: 
вставьте в терминал <code>npm install -g localtunnel</code>. 
<p><b>Если у вас нет пакетного менеджера npm, установите его командой: <code>sudo apt install npm </code></b>.</p> 
После установки <code>localtunnel</code> получим временный публичный <u>https url</u>, командой: 
<code>lt --port 8082</code> <i>(указал не стадратный порт на случай, если ваш 8080 уже чем-то занят, и дабы не 
заниматься поисками
- сразу зададим свободный порт)</i>, который будет проксировать входящие запросы к нам на локальный сервер.</li>
Полученный url необходимо вставить в файл <code>.env.local</code> в переменную <code>WEBHOOK_HOST</code>.
Должно получиться примерно: <code>WEBHOOK_HOST=https://strong-chairs-drive.loca.lt</code>
   <li>Убедитесь, что в файле <code>docker-compose.yml</code> для сервиса <b>bot</b> указаны порты: 
<code>8082:8080</code></li>
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
указывайте разные порты, но я предполагаю, что расписывать как это работает - будет неуместно в описании данного проекта.
Во-вторых, предлагается указать следующую маршрутизацию:
<p>Вот как выглядят мои настройки хостового nginx, расположен по пути: <code>/etc/nginx/conf.d/pqpq.pw.conf</code></p>

    server { # этот блок переадресовывает запросы по http на https 
    listen 80; 
    server_name pqpq.pw;
    return 301 https://$host$request_uri;
    }

    server {
    listen 443 ssl;
    server_name pqpq.pw;

      # это часть указывает на сертификаты ssl
    ssl_certificate /etc/letsencrypt/live/pqpq.pw/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/pqpq.pw/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    location /webhook { # этот блок проксирует вебхуки на соответствующий обработчик веб приложения на локалхост контейнер,
      # который слушает 8080 порт
        proxy_pass http://localhost:8080/webhook;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location / {
      # этот блок не обязателен, т.к. он может вести куда угодно, для бота он не нужен
        proxy_pass http://localhost:8080/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location /s/ {
      # этот блок обрабатывает редирект по нашим сокращенным ссылкам
        proxy_pass http://localhost:8080/s/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    } }


</li>
<li> Получите api-key у бота <code>@BotFather</code>.</li>
<li>Клонируйте репозиторий <code>git clone https://github.com/artem-sitd/link-shortener.git</code></li>
<li>Переименуйте файл <code>env.template</code> в <code>.env</code>., вставьте ваш api-key напротив переменной 
<code>telegram_api_key</code> после знака <code>=</code>.
   Должно получиться что-то вроде <code>telegram_api_key=7711:A74hGffoOomZMsPJTdoH_jbLIR6A4q8_bM3jM</code></li>
<li><code>WEBHOOK_HOST=</code> сюда вставьте ваш URL https и сюда тоже самое <code>main_domain=</code></li>
   <li>В модуле <code>settings.py</code> в функции <b>get_env_file</b> необходимо присвоить переменной <b>local</b>
 значение <b>False</b>, для использования правильного файла для переменных окружения. 
Должно получиться: <code>def get_env_file(local: bool = False) -> Path:</code></li>
<li>Убедитесь, что в файле <code>docker-compose.yml</code> для сервиса <b>bot</b> указаны порты, соответствующие
 настройкам хостового nginx (например): <code>8080:8080</code></li>
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
<li>Изолировать монго от внешнего мира: 
<ol>
<li>убрать публикацию порта для mongo внутри docker-compose</li>
<li>Заранее создать пользователя и пароль для чтения, записи в <b>конкретную</b> базу, указав их данные в 
переменную окружения. <b>Наделив ограниченными правами!</b></li>
<li>ограничить права для стандартного пользователя admin, либо отключить его</li>
<li>создать одинаковую сеть для взаимодействующих между собой контейнеров (сделано)</li>
<li>Подключаться к базе через имя сервиса docker контейнера: <code>environment:
      MONGO_URI: mongodb://admin:adminpassword@mongo:27017/your_database_name</code></li>
<li>Данные мероприятия направлены для защиты БД от типичной атаки:

    READ__ME_TO_RECOVER_YOUR_DATA> db.README.find()
    [{
    _id: ObjectId('67b8ffad478a9b8d47'),
    content: 'All your data is backed up. You must pay 0.0045 BTC to 
    bc1qt3zrm0va2g5adut9pnwka76yrzwjp In 48 hours, your data 
      will be publicly disclosed and deleted. (more information: go to 
      htt://2o.wn/mb)After paying send mail to us: ramler+1qx4@onionmail.org
      and we will provide a link for you to download your data. 
      Your DBCODE is: 1OX'
    }]
</li>
</ol></li>
</ul>



<h2 id="commands">Общие Полезные команды</h2>


<ul> 
<li>Установка вебхуков <code>npm install -g localtunnel</code></li>
<li>Получение локальных вебхуков: <code>lt --port 8080</code></li>
<li>Проверить статус вебхуков <code>curl https://api.telegram.org/bot"your_api_key_bot"/getWebhookInfo</code> без кавычек</li>
<li> <code></code></li>
<li> <code></code></li>

</ul>