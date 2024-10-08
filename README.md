# Flower Delivery: Django-based Flower Shop with Telegram Bot Integration

## Описание проекта

Этот проект представляет собой веб-приложение для онлайн-заказа цветов. Приложение разработано с использованием Django и включает интеграцию с телеграм-ботом для управления заказами, аналитики и уведомлений. Клиенты могут оформлять заказы, просматривать историю своих покупок и управлять профилем. Администраторы могут отслеживать заказы, управлять отчетами и анализировать продажи.

---

## Основные функции

### Веб-сайт:

- **Регистрация и авторизация пользователей:**
  Пользователи могут регистрироваться и авторизоваться для доступа к личному кабинету и истории заказов.

- **Просмотр каталога цветов:**
  Каталог позволяет пользователям просматривать доступные товары с возможностью фильтрации и сортировки.

- **Добавление цветов в корзину:**
  Пользователь может выбрать цветы и добавить их в корзину для дальнейшего оформления заказа.

- **Оформление заказа:**
  Процесс оформления заказа включает ввод данных для доставки (адрес, имя получателя, контактный телефон) и выбор метода оплаты.

- **Просмотр истории заказов:**
  Личный кабинет содержит историю заказов, включая информацию о доставке и статусе каждого заказа.

- **Управление статусами заказов (администратор):**
  Администраторы имеют возможность изменять статус заказа через административную панель.

- **Возможность повторного заказа:**
  Пользователи могут легко повторить заказ той же позиции из каталога.

- **Отзывы и рейтинги:**
  Пользователи могут оставлять отзывы на продукты и выставлять рейтинг.

- **Аналитика и отчеты по заказам (администратор):**
  Система предоставляет отчетность по продажам, заказам и активности пользователей.

### Telegram бот:

- **Получение заказов:**
  Бот позволяет получать уведомления о новых заказах с информацией о букетах и данных для доставки.

- **Уведомления о статусе заказа:**
  Пользователи получают уведомления о изменении статуса их заказа.

- **Аналитика и отчеты:**
  Бот предоставляет краткую аналитику по заказам и продажам для администраторов.


---
## Структура проекта

```bash
flower_delivery/
├── apps/
│   ├── analytics/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── forms.py
│   │   ├── models.py
│   │   ├── urls.py
│   │   ├── views.py
│   │   ├── tests.py
│   │   ├── templates/
│   │   │   └── analytics/
│   │   │       ├── analytics.html
│   │   │       ├── analytics_overview.html
│   │   │       ├── report_detail.html
│   │   │       ├── report_form.html
│   │   │       ├── report_list.html
│   │   │       └── report_management.html
│   ├── cart/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── context_processors.py
│   │   ├── models.py
│   │   ├── urls.py
│   │   ├── views.py
│   │   ├── tests.py
│   │   ├── templates/
│   │   │   └── cart/
│   │   │       ├── cart.html
│   │   │       └── checkout.html
│   ├── catalog/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── context_processors.py
│   │   ├── models.py
│   │   ├── urls.py
│   │   ├── views.py
│   │   ├── tests.py
│   │   ├── templates/
│   │   │   └── catalog/
│   │   │       ├── home.html
│   │   │       ├── product_detail.html
│   │   │       ├── product_list.html
│   ├── orders/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── forms.py
│   │   ├── models.py
│   │   ├── urls.py
│   │   ├── views.py
│   │   ├── tests.py
│   │   ├── templates/
│   │   │   └── orders/
│   │   │       ├── create_order.html
│   │   │       ├── order_list.html
│   │   │       ├── order_management.html
│   │   │       ├── update_order_status.html
│   ├── reviews/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── forms.py
│   │   ├── models.py
│   │   ├── urls.py
│   │   ├── views.py
│   │   ├── tests.py
│   │   ├── templates/
│   │   │   └── reviews/
│   │   │       ├── product_reviews.html
│   ├── telegram_bot/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── bot.py
│   │   ├── forms.py
│   │   ├── keyboards.py
│   │   ├── urls.py
│   │   ├── views.py
│   │   ├── tests.py
│   │   ├── management/
│   │   │   └── commands/
│   │   │       ├── runserverandbot.py
│   │   │       └── startbot.py
│   │   ├── templates/
│   │   │   └── telegram_bot/
│   │   │       ├── bot_info.html
│   ├── users/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── forms.py
│   │   ├── models.py
│   │   ├── urls.py
│   │   ├── views.py
│   │   ├── tests.py
│   │   ├── templates/
│   │   │   └── users/
│   │   │       ├── login.html
│   │   │       ├── profile.html
│   │   │       ├── profile_edit.html
│   │   │       ├── register.html
├── flower_delivery/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
├── manage.py
├── .env
├── requirements.txt
├── static/
│   └── css/
│       └── styles.css
├── media/
```

## Пояснение

- **`apps/`** — Каталог, где содержатся все приложения проекта.

  - **`analytics/`** — Приложение для аналитики и отчетов по заказам.
  - **`cart/`** — Приложение для корзины покупок.
  - **`catalog/`** — Приложение для управления товарами и каталогом.
  - **`orders/`** — Приложение для управления заказами.
  - **`reviews/`** — Приложение для отзывов о товарах.
  - **`telegram_bot/`** — Приложение для интеграции с Telegram ботом.
  - **`users/`** — Приложение для управления пользователями и аутентификацией.

- **`flower_delivery/`** — Основная директория проекта, где находятся настройки и конфигурации проекта.

  - **`settings.py`** — Настройки Django.
  - **`urls.py`** — Основной файл маршрутизации.
  - **`wsgi.py` и `asgi.py`** — Файлы для запуска приложения через WSGI или ASGI.

- **`manage.py`** — Стандартный скрипт для управления проектом Django.

- **`.env`** — Файл с переменными окружения, включая токен Telegram бота.

- **`requirements.txt`** — Файл со списком зависимостей Python.

- **`static/`** — Каталог для статических файлов (CSS, JS, изображения).

- **`media/`** — Каталог для загружаемых файлов (например, изображения продуктов).

---
## Архитектура системы

### Общие сведения

- **Технологии:**
  Веб-приложение реализовано с использованием Django.
  Серверная часть написана на языке Python.

### Модули и подсистемы

- **Модуль регистрации и авторизации:**
  Отвечает за управление пользователями, включая регистрацию, авторизацию и восстановление пароля.

- **Модуль каталога товаров:**
  Реализует функционал просмотра товаров, включая фильтрацию и сортировку по различным критериям.

- **Модуль оформления заказа:**
  Позволяет пользователям выбрать товары, ввести данные для доставки и подтвердить заказ.

- **Модуль управления заказами:**
  Администратор управляет статусами заказов и отслеживает их выполнение.

- **Модуль отзывов и рейтингов:**
  Пользователи могут оставлять отзывы на товары и оценивать их по пятизвездочной шкале.

- **Модуль аналитики и отчетов:**
  Включает отчеты для администраторов по продажам, активности пользователей и статусам заказов.

---

## Установка

### Шаг 1: Клонирование репозитория

```bash
git clone https://github.com/username/flower_delivery.git
cd flower_delivery
```

### Шаг 2: Создание виртуального окружения и установка зависимостей

Создайте виртуальное окружение и активируйте его:

```bash
python -m venv venv
source venv/bin/activate  # Для Windows: venv\Scripts\activate
```

### Установка зависимостей

Установите зависимости:

```bash
pip install -r requirements.txt
```

### Шаг 3: Настройка .env файла

Создайте файл `.env` в корне проекта и добавьте в него токен вашего Telegram бота:

```plaintext
TELEGRAM_BOT_TOKEN='ваш_токен'
```

### Шаг 4: Миграции и создание суперпользователя

Примените миграции базы данных:

```bash
python manage.py migrate
```

### Создайте суперпользователя для доступа к админ-панели:

```bash
python manage.py createsuperuser
```

### Шаг 5: Запуск проекта

Для запуска проекта, одновременно запустите сервер Django и телеграм-бота:

```bash
python manage.py runserverandbot
```

### Шаг 6: Доступ к приложению

Приложение будет доступно по адресу [http://127.0.0.1:8000](http://127.0.0.1:8000). 
В админ-панель можно войти по адресу [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin), используя данные суперпользователя.

---
## Запуск тестов

Для запуска тестов в различных приложениях используйте следующие команды:

```bash
python manage.py test apps.analytics
python manage.py test apps.cart
python manage.py test apps.catalog
python manage.py test apps.orders
python manage.py test apps.reviews
python manage.py test apps.telegram_bot
python manage.py test apps.users
```
---

## Использование

### Телеграм-бот

После запуска бота вы можете взаимодействовать с ним, используя следующие команды:

- **/start** — Приветственное сообщение.
- **/link <номер телефона>** — Привязка аккаунта Telegram к профилю на сайте.
- **/orders_all** — Получение всех заказов.
- **/orders** — Получение последних 5 заказов.
- **/info <номер заказа>** — Получение информации о заказе.
- **/analytics** — Получение аналитических отчетов по заказам.

### Пример использования

- **Регистрация:** Зайдите на сайт и зарегистрируйтесь, указав ваш номер телефона.
- **Привязка аккаунта:** Используйте команду `/link` в Telegram, чтобы привязать ваш аккаунт на сайте к Telegram.
- **Оформление заказа:** Выберите товар, добавьте его в корзину и оформите заказ.
- **Получение информации:** Используйте команду `/info <номер заказа>` в Telegram для получения информации о заказе.

---
## Стек технологий

- **Backend:** Django 5.1

- **Frontend:** Bootstrap

- **База данных:** SQLite (по умолчанию)

- **Интеграция с Telegram:** Aiogram 3.x

- **Аутентификация:** Custom User Model с поддержкой телефонных номеров

- **Асинхронные задачи:** Channels (ASGI)

- **API:**
  - **Yandex.Maps API:** Используется для выбора адресов на карте в веб-приложении.
---

## Лицензия

Этот проект лицензирован под лицензией MIT. Полный текст лицензии приведен ниже.

---

### Лицензия MIT

Разрешается любое использование, копирование, изменение, объединение, публикация и распространение этого программного обеспечения и сопутствующей документации (включая, но не ограничиваясь, исходным кодом) при условии, что следующие условия выполнены:

1. Все вышеуказанные уведомления о авторских правах и уведомления о лицензии должны быть включены во все копии или значительные части данного программного обеспечения.

2. Это программное обеспечение предоставляется "как есть", без каких-либо гарантий, явных или подразумеваемых, включая, но не ограничиваясь, подразумеваемыми гарантиями товарной пригодности и пригодности для конкретной цели. Ни при каких обстоятельствах авторы или правообладатели не несут ответственности за любой иск, убытки или другие обязательства, будь то в результате договора, деликта или иным образом, возникшие из, в связи с или в связи с использованием этого программного обеспечения или иными действиями по его использованию.

---








