# website

Бэкенд для простого новостного сайта.

Возможности:
- Регистрация пользователя;
- Хранение дополнительных данных о пользователе: телефон, город, флаг верификации, количество опубликованных новостей;
- Аутентификация пользователя;
- Просмотр данных аккаунта;
- Пользователи разделены на три группы: обычные пользователи, верифицированные пользователи и модераторы. Верифицированным пользователям доступна возможность создания новостей (в Личном кабинете есть раздел "Создать новость"). Публикация новости возможна только после одобрения модератором;

  Верифицированные - созданы от модели User, через функционал админки добавляется группа 'Верифицированный пользователь' (Can add news, can view news), доступ к админке отсутствует. Новость, созданная таким пользователем, имеет статус Published=False и не видна на сайте.
  Модераторы - созданы от модели User, через функционал админки добавляется группа 'Модератор' (Can add news, can view news, доступ к админке разрешен). В админке могут видеть все новости. Через админку в новости могут присваивать статус Published=True. После этого новость считается опубликованной и видна на сайте всем.

  Для автоматического создания группы Верифицированный пользователь и Модератор создан файл миграций 0003_auto_20210315_2228.py, который при первом запуске команды python3 manage.py migrate выполнит все необходимые действия.

- К новостям можно добавлять комментарии (форма для комментариев и сами комментарии находятся под текстом новости. если комментарий оставляет аутентифицированный пользователь, то в шаблоне выводится его имя. для неаутентифицированных пользователей - 'аноним');
- Есть возможность указать тег для новости и затем фильтровать список новостей по нему;
