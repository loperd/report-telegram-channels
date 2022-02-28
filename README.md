## Report dirty Telegram channels

1. Установите Docker https://docs.docker.com/get-docker/
2. Залогиньтесь в https://my.telegram.org
3. Перейдите в API development tools и заполните форму.
4. Вы получите api_id и api_hash. В настоящий момент к одному номеру телефона может быть привязан только один api_id.
5. У вас попросит бот токен или номер телефона аккаунта, введите его.
6. Затем попросит код который придёт в телеграм, введите его.
7. (optional) Если включена двухфакторка - у вас спросит пароль, введите его!

```bash
$ docker run -it --rm loperd/report-tg-channels <API_ID> <API_HASH> https://raw.githubusercontent.com/loperd/report-telegram-channels/master/dirty_channels.txt
```
При первом запуске скрипт спросит номер телефона и попросит ввести одноразовый код, который придет в Telegram
для подтверждения аккаунта. При следующих запусках скрипт уже не будут ничего спрашивать.

Пример правильной отработки скрипта:
```bash
$ docker run -it --rm loperd/report-tg-channels <API_ID> <API_HASH> https://raw.githubusercontent.com/loperd/report-telegram-channels/master/dirty_channels.txt
Please enter your phone (or bot token): +380XXX
Please enter the code you received: 123456
Please enter your password: 123456
Signed in successfully as Anonymous
https://t.me/warjournaltg: True
```

###  Как получить `api_id` и `api_hash`
1. Залогиньтесь в https://my.telegram.org.
2. Перейдите в `API development tools` и заполните форму, как показано на экране:

![Telegram form](./docs/telegram_form.png)
3. Вы получите `api_id` и `api_hash`. В настоящий момент к одному номеру телефона может быть привязан только один `api_id`.

### ВАЖНО! Причина жалобы

В файле `messages.txt` находится список причин для жалобы. На каждый канал рандомно берётся одна. В теории у телеги есть 
защита от спама, поэтому не поленитесь в этот файл написать своих формулировок причин.

### Автообновление целей

Удалите файл `dirty_channels.txt` (список каналов) локально и запустите скрипт. Свежий список каналов будет скачан из 
репозитория автоматически.
