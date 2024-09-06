from aiogram import Bot, Dispatcher, Router
from aiogram.types import Message
from aiogram.filters import Command, CommandObject
from aiogram.types import CallbackQuery
from asgiref.sync import sync_to_async
from django.conf import settings
from apps.orders.models import Order, OrderDetail
from apps.users.models import User
from apps.analytics.models import Report
from .keyboards import main_menu
import re


bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
dp = Dispatcher()
router = Router()

PHONE_REGEX = re.compile(r"^\+7\d{10}$")


@router.callback_query(lambda c: c.data == "confirm")
async def process_confirm(callback_query: CallbackQuery):
    await callback_query.answer("Вы подтвердили действие!")


@router.callback_query(lambda c: c.data == "cancel")
async def process_cancel(callback_query: CallbackQuery):
    await callback_query.answer("Действие отменено!")


@router.message(Command("start"))
async def start_command(message: Message):
    await message.answer(
        "Добро пожаловать в бот для заказа доставки цветов! Выберите нужную команду:",
        reply_markup=main_menu(),
    )


@router.message(Command("link"))
async def link_command(message: Message, command: CommandObject):
    if command.args is None:
        await message.answer(
            "Пожалуйста, введите номер телефона после команды /link, например: /link +71234567890"
        )
        return

    phone_number = command.args.strip()

    if not PHONE_REGEX.match(phone_number):
        await message.answer(
            "Пожалуйста, введите номер телефона в правильном формате: +7XXXXXXXXXX"
        )
        return

    user = await sync_to_async(
        lambda: User.objects.filter(phone_number=phone_number).first()
    )()

    if user:
        user.telegram_id = message.from_user.id
        await sync_to_async(user.save)()
        await message.answer("Ваш аккаунт успешно привязан к Telegram!")
    else:
        await message.answer(
            "Пользователь с таким номером телефона не зарегистрирован."
        )


@router.message(Command("analytics"))
async def analytics_command(message: Message):
    user_id = message.from_user.id

    user = await sync_to_async(User.objects.filter(telegram_id=user_id).first)()
    if not user:
        await message.answer(
            "Вы не привязали свой аккаунт. Введите /link для привязки."
        )
        return

    # Выполняем синхронные запросы к базе данных через sync_to_async
    reports = await sync_to_async(
        lambda: list(Report.objects.filter(order__user=user))
    )()

    if reports:
        response = "Ваши отчеты:\n"
        for report in reports:
            order_id = await sync_to_async(
                lambda: report.order.id
            )()  # Получаем id заказа через sync_to_async
            response += (
                f"Отчет #{report.id} за {report.report_date}:\n"
                f"Заказ #{order_id} - Прибыль: {report.profit} USD - Расходы: {report.expenses} USD\n"
            )
        await message.answer(response)
    else:
        await message.answer("Отчеты не найдены.")


async def main():
    if not router.parent_router:
        dp.include_router(router)
    await dp.start_polling(bot)


@router.message(Command("orders_all"))
async def my_orders_command(message: Message):
    user_id = message.from_user.id

    user = await sync_to_async(User.objects.filter(telegram_id=user_id).first)()

    if not user:
        await message.answer(
            "Ваш аккаунт не привязан к Telegram. Введите /link для привязки."
        )
        return

    orders = await sync_to_async(lambda: list(Order.objects.filter(user=user)))()

    if not orders:
        await message.answer("У вас нет заказов.")
        return

    response = "Ваши заказы:\n"
    for order in orders:
        response += f"Заказ №{order.id}, статус: {order.get_status_display()}, дата заказа: {order.created_at.strftime('%d-%m-%Y')}\n"

    await message.answer(response)


@router.message(Command("orders"))
async def my_recent_orders_command(message: Message):
    user_id = message.from_user.id

    user = await sync_to_async(User.objects.filter(telegram_id=user_id).first)()

    if not user:
        await message.answer(
            "Ваш аккаунт не привязан к Telegram. Введите /link для привязки."
        )
        return

    recent_orders = await sync_to_async(
        lambda: list(Order.objects.filter(user=user).order_by("-created_at")[:5])
    )()

    if not recent_orders:
        await message.answer("У вас нет заказов.")
        return

    response = "Ваши последние 5 заказов:\n"
    for order in recent_orders:
        response += f"Заказ №{order.id}, статус: {order.get_status_display()}, дата заказа: {order.created_at.strftime('%d-%m-%Y')}\n"

    await message.answer(response)


@router.message(Command("info"))
async def order_info_command(message: Message, command: CommandObject):
    user_id = message.from_user.id

    if not command.args:
        await message.answer("Пожалуйста, укажите номер заказа. Пример: /info 51")
        return

    try:
        order_id = int(command.args.strip())
    except ValueError:
        await message.answer("Номер заказа должен быть числом. Пример: /info 51")
        return

    user = await sync_to_async(User.objects.filter(telegram_id=user_id).first)()

    if not user:
        await message.answer(
            "Ваш аккаунт не привязан к Telegram. Введите /link для привязки."
        )
        return

    order = await sync_to_async(Order.objects.filter(user=user, id=order_id).first)()

    if not order:
        await message.answer(f"У вас нет заказа с номером {order_id}.")
        return

    order_details = await sync_to_async(
        lambda: list(OrderDetail.objects.filter(order=order))
    )()

    products = ""
    total_sum = 0

    for detail in order_details:
        product_name = await sync_to_async(
            lambda: detail.product.name
        )()  # Асинхронное получение имени продукта
        products += f"- {product_name} - {detail.quantity} шт.\n"
        total_sum += detail.total_price

    response = f"""
    Дата заказа: {order.created_at.strftime('%d-%m-%Y')}
    Номер получателя: {order.phone_number}
    Адрес доставки: {order.delivery_address}

    Перечень товаров:
    {products}

    На сумму: {total_sum} USD
    """

    await message.answer(response)


@router.message(Command("help"))
async def help_command(message: Message):
    help_text = (
        "Список доступных команд:\n\n"
        "/start - Запуск бота и приветственное сообщение.\n"
        "/link <номер телефона> - Привязка вашего аккаунта Telegram к вашему аккаунту на сайте.\n"
        "  Пример: /link +71234567890\n\n"
        "/orders_all - Получение всех ваших заказов.\n"
        "/orders - Получение последних 5 заказов.\n"
        "/info <номер заказа> - Получение информации о конкретном заказе.\n"
        "  Пример: /info 123\n\n"
        "/analytics - Получение отчета по заказам и аналитике.\n"
    )
    await message.answer(help_text, reply_markup=main_menu())
